import { Injectable } from '@angular/core';
import { Dictionary } from '@ngrx/entity';

import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';

@Injectable({
  providedIn: 'root'
})
export class CalendarService {

  constructor() { }

  getStudentOrClassFromEntity() {
    
  }

  formatCalendarEvents(
    scheduledClassesInfo: ScheduledClassModel[] | undefined,
    //lowBillingAccntHrs: number[]
  ) {
    let i;
    let events = [];
    if (scheduledClassesInfo) {
      for (i=0; i < scheduledClassesInfo.length; i++) {
        var schedulingObj = {
          title: `${scheduledClassesInfo[i].student_or_class}
          ${scheduledClassesInfo[i].student_or_class}`,
          date: scheduledClassesInfo[i].date,
          start: `${scheduledClassesInfo[i].date}T${scheduledClassesInfo[i].start_time}`,
          end: `${scheduledClassesInfo[i].date}T${scheduledClassesInfo[i].finish_time}`,
          allDay : false,
          color: '#0098da',
        }

        //if (lowBillingAccntHrs.indexOf(
        //    scheduledClassesInfo[i].student_billing_account) !== -1) {
        //  schedulingObj.color = '#dc3545'
        //}
        events.push(schedulingObj)
      }
    }
    return events
  }



}
