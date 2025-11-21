"""
Scheduler Module for Autolauncher.
Handles task scheduling using APScheduler's BackgroundScheduler.
Executes programs at scheduled times without blocking the Qt event loop.
"""

import subprocess
from datetime import datetime
from typing import Dict, List
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from logger import get_logger

logger = get_logger(__name__)


class TaskScheduler:
    """
    Manages task scheduling using APScheduler.
    Runs in the background without interfering with the Qt event loop.
    """
    
    def __init__(self):
        """
        Initialize the TaskScheduler with a BackgroundScheduler.
        """
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logger.info("TaskScheduler initialized and started")
    
    def add_job(self, task: Dict) -> bool:
        """
        Add a scheduled job from task data.
        
        Args:
            task: Dictionary containing task data with keys:
                  - id: Unique task identifier
                  - name: Task name
                  - program_path: Path to the executable
                  - schedule_time: Scheduled time (ISO format string)
                  - recurrence: Recurrence type (Once, Daily, Weekly, Monthly)
                  - enabled: Boolean indicating if task is active
                  
        Returns:
            True if job was added successfully, False otherwise
        """
        try:
            if not task.get('enabled', True):
                logger.debug(f"Task {task['name']} is disabled, skipping")
                return False
            
            # Parse schedule time
            schedule_time = datetime.fromisoformat(task['schedule_time'])
            recurrence = task.get('recurrence', 'Once')
            
            # Create job ID from task ID
            job_id = f"task_{task['id']}"
            
            # Remove existing job if it exists
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
                logger.debug(f"Removed existing job {job_id}")
            
            # Determine trigger based on recurrence
            trigger = None
            
            if recurrence == 'Daily':
                # Run every day at the specified time
                trigger = CronTrigger(
                    hour=schedule_time.hour,
                    minute=schedule_time.minute,
                    second=schedule_time.second
                )
            elif recurrence == 'Weekly':
                # Run every week on the specified day at the specified time
                # day_of_week: 0=Mon, 6=Sun
                trigger = CronTrigger(
                    day_of_week=schedule_time.weekday(),
                    hour=schedule_time.hour,
                    minute=schedule_time.minute,
                    second=schedule_time.second
                )
            elif recurrence == 'Monthly':
                # Run every month on the specified day at the specified time
                trigger = CronTrigger(
                    day=schedule_time.day,
                    hour=schedule_time.hour,
                    minute=schedule_time.minute,
                    second=schedule_time.second
                )
            else: # Once
                # Don't schedule tasks in the past for one-time execution
                if schedule_time <= datetime.now():
                    logger.warning(f"Task {task['name']} scheduled time is in the past, skipping")
                    return False
                
                trigger = DateTrigger(run_date=schedule_time)
            
            # Add the job
            self.scheduler.add_job(
                func=self._execute_task,
                trigger=trigger,
                args=[task],
                id=job_id,
                name=task['name'],
                replace_existing=True
            )
            
            logger.info(f"Scheduled task '{task['name']}' ({recurrence}) for {schedule_time}")
            return True
            
        except ValueError as e:
            logger.error(f"Invalid schedule time format for task {task.get('name')}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error adding job for task {task.get('name')}: {e}")
            return False
    
    def remove_job(self, task_id: int) -> bool:
        """
        Remove a scheduled job.
        
        Args:
            task_id: ID of the task whose job should be removed
            
        Returns:
            True if job was removed, False otherwise
        """
        try:
            job_id = f"task_{task_id}"
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
                logger.info(f"Removed job for task ID {task_id}")
                return True
            else:
                logger.debug(f"No job found for task ID {task_id}")
                return False
        except Exception as e:
            logger.error(f"Error removing job for task ID {task_id}: {e}")
            return False
    
    def update_job(self, task: Dict) -> bool:
        """
        Update a scheduled job (removes old and adds new).
        
        Args:
            task: Updated task dictionary
            
        Returns:
            True if job was updated successfully, False otherwise
        """
        self.remove_job(task['id'])
        return self.add_job(task)
    
    def execute_immediately(self, task: Dict) -> bool:
        """
        Execute a task immediately without affecting its schedule.
        
        Args:
            task: Task dictionary
            
        Returns:
            True if execution started, False otherwise
        """
        try:
            logger.info(f"Manual execution requested for task '{task['name']}'")
            # Run in background to avoid blocking
            self.scheduler.add_job(
                func=self._execute_task,
                trigger=DateTrigger(run_date=datetime.now()),
                args=[task],
                name=f"manual_{task['name']}",
                misfire_grace_time=60
            )
            return True
        except Exception as e:
            logger.error(f"Failed to execute task immediately: {e}")
            return False

    def _execute_task(self, task: Dict):
        """
        Execute a scheduled task by launching the program.
        
        Args:
            task: Task dictionary containing the program path
        """
        program_path = task['program_path']
        task_name = task['name']
        
        logger.info(f"Executing task '{task_name}': {program_path}")
        
        try:
            # Use os.startfile to execute the file using the Windows shell
            # This ensures .lnk files (shortcuts) are handled correctly with all their properties
            # (arguments, working directory, compatibility settings, etc.)
            import os
            os.startfile(program_path)
            
            logger.info(f"Successfully launched '{task_name}'")
            
        except FileNotFoundError:
            logger.error(f"Program not found for task '{task_name}': {program_path}")
        except PermissionError:
            logger.error(f"Permission denied for task '{task_name}': {program_path}")
        except Exception as e:
            logger.error(f"Failed to execute task '{task_name}': {e}")
    
    def get_all_jobs(self) -> List:
        """
        Get all scheduled jobs.
        
        Returns:
            List of Job objects
        """
        return self.scheduler.get_jobs()
    
    def shutdown(self):
        """
        Shutdown the scheduler gracefully.
        """
        try:
            self.scheduler.shutdown(wait=False)
            logger.info("TaskScheduler shut down successfully")
        except Exception as e:
            logger.error(f"Error shutting down scheduler: {e}")
    
    def get_next_run_time(self, task_id: int) -> datetime:
        """
        Get the next run time for a specific task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            datetime object of next run time, or None if not scheduled
        """
        try:
            job_id = f"task_{task_id}"
            job = self.scheduler.get_job(job_id)
            if job:
                return job.next_run_time
        except Exception as e:
            logger.error(f"Error getting next run time for task ID {task_id}: {e}")
        
        return None
