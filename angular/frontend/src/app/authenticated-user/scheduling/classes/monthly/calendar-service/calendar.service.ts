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
    scheduledClasses: ScheduledClassModel[] | undefined,
    //lowBillingAccntHrs: number[]
  ) {
    console.log('**********calling the format method**********')
    console.log(scheduledClasses);
    let i;
    let events = [];
    if (scheduledClasses) {
      for (i=0; i < scheduledClasses.length; i++) {
        var schedulingObj = {
          title: `${scheduledClasses[i].student_or_class}
          ${scheduledClasses[i].student_or_class}`,
          date: scheduledClasses[i].date,
          start: `${scheduledClasses[i].date}T${scheduledClasses[i].start_time}`,
          end: `${scheduledClasses[i].date}T${scheduledClasses[i].finish_time}`,
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
