import { Component, Input, OnInit } from '@angular/core';

import { 
  calculateTimeStringsDifferenceinNumbers 
} from 'src/app/shared-utils/date-time.util';

@Component({
  selector: 'app-time-in-hours',
  standalone: false,
  templateUrl: './time-in-hours.component.html',
  styleUrl: './time-in-hours.component.css'
})
export class TimeInHoursComponent implements OnInit {

  @Input() startTime: string;
  @Input() finishTime: string;

  timeInHours: number | undefined = undefined;

  ngOnInit(): void {
    console.log("***********Debugging************")
    console.log(`Start time: ${this.startTime}`)
    console.log(`Finish time: ${this.finishTime}`)
    this.timeInHours = calculateTimeStringsDifferenceinNumbers(
      this.startTime.slice(0, -3), this.finishTime.slice(0, -3)
    );
    console.log(`Result: ${this.timeInHours}`)
  }

}
