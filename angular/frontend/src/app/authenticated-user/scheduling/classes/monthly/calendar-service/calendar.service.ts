import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { first } from 'rxjs';

import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { 
  selectStudentOrClassById 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { 
  StudentsOrClassesState 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';

@Injectable({
  providedIn: 'root'
})
export class CalendarService {

  constructor(private store: Store<StudentsOrClassesState>) { }

  formatCalendarEvents(
    scheduledClasses: ScheduledClassModel[] | undefined,
  ) {
    let events = [];
    if (scheduledClasses) {
      for (let i=0; i < scheduledClasses.length; i++) {
        let schedulingObj = {
          title: `Inactive Account`,
          date: scheduledClasses[i].date,
          start: `${scheduledClasses[i].date}T${scheduledClasses[i].start_time}`,
          end: `${scheduledClasses[i].date}T${scheduledClasses[i].finish_time}`,
          allDay : false,
          color: '#0098da',
        }
        let studentOrClass: StudentOrClassModel | undefined;
        this.store.select(selectStudentOrClassById(
          scheduledClasses[i].student_or_class)
        ).pipe(first()).subscribe((res) => {
          studentOrClass = res;
        })
        if (studentOrClass) {
          schedulingObj.title = studentOrClass.template_str;
          if (studentOrClass.purchased_class_hours) {
            if (studentOrClass.purchased_class_hours <= 3) {
              schedulingObj.color = '#dc3545';
            }
          }
        }
        events.push(schedulingObj)
      }
    }
    return events
  }



}
