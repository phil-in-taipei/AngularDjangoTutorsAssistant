import { Injectable } from '@angular/core';
//import { Dictionary } from '@ngrx/entity';
import { select, Store } from '@ngrx/store';
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
    console.log('**********calling the format method**********')
    console.log(scheduledClasses);
    let i;
    let events = [];
    if (scheduledClasses) {
      for (i=0; i < scheduledClasses.length; i++) {
        let studentOrClass: StudentOrClassModel | undefined;
        this.store
        .select(selectStudentOrClassById(scheduledClasses[i].student_or_class))
        .pipe(first()) // Automatically unsubscribes after the first value
        .subscribe((res) => {
          studentOrClass = res; // Assuming 'this.studentOrClass' is a class property
        })
        console.log(studentOrClass);

        var schedulingObj = {
          title: `Inactive Account`,
          date: scheduledClasses[i].date,
          start: `${scheduledClasses[i].date}T${scheduledClasses[i].start_time}`,
          end: `${scheduledClasses[i].date}T${scheduledClasses[i].finish_time}`,
          allDay : false,
          color: '#0098da',
        }
        if (studentOrClass) {
          schedulingObj.title = studentOrClass.template_str;
          if (studentOrClass.purchased_class_hours) {
            if (studentOrClass.purchased_class_hours < 4) {
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
