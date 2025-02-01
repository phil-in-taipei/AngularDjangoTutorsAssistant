import { Component, Input, OnInit } from '@angular/core';
import { CalendarOptions } from '@fullcalendar/core';
import interactionPlugin from '@fullcalendar/interaction';
import timeGridPlugin from '@fullcalendar/timegrid';
import dayGridPlugin from '@fullcalendar/daygrid';
import { Router } from '@angular/router';

import { CalendarService } from '../calendar-service/calendar.service';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';

@Component({
  selector: 'app-calendar-schedule',
  standalone: false,
  templateUrl: './calendar-schedule.component.html',
  styleUrl: './calendar-schedule.component.css'
})
export class CalendarScheduleComponent implements OnInit {

  calendarOptions: CalendarOptions;

  Events: any[] = []
  @Input() scheduledClasses: ScheduledClassModel[];
  @Input() monthlyDateRange: [string, string];

  constructor(
    private calendarService: CalendarService,
    private router: Router,
  ) { }

  ngOnInit(): void {
    console.log('in the calendar component, these are the scheduled classes:')
    console.log(this.scheduledClasses);
    this.Events = this.calendarService.formatCalendarEvents(this.scheduledClasses);
    this.calendarOptions = {
      plugins: [
            dayGridPlugin,
            interactionPlugin,
            timeGridPlugin,
          ],
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,listWeek', // timeGridDay,
      },
      eventTextColor: 'black',
      initialView: 'dayGridMonth',
      //datesSet: this.onDateClick.bind(this),  
      dateClick: (arg) => {  // Use this syntax
        this.onDateClick(arg);
      },
      validRange: {
        start: this.monthlyDateRange[0],
        end: this.monthlyDateRange[1]
      },
      events: this.Events,
    };
   console.log(this.calendarOptions);
   console.log(this.Events);
  }

  onDateClick(res: any) {
    //alert('Clicked on date : ' + res.dateStr);
    console.log(res)
    this.router.navigate(['/', 'authenticated-user', 'scheduling', 'schedule-daily', res.dateStr]);
  }

  setDefaultDate() {
    this.calendarOptions.validRange = {
      start: this.monthlyDateRange[0],
      end: this.monthlyDateRange[1]
    }
  }

}
