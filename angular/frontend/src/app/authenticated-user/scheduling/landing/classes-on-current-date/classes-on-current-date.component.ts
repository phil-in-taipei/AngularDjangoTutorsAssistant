import { Component, Input } from '@angular/core';

import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';

@Component({
  selector: 'app-classes-on-current-date',
  standalone: false,
  templateUrl: './classes-on-current-date.component.html',
  styleUrl: './classes-on-current-date.component.css'
})
export class ClassesOnCurrentDateComponent {

  @Input() scheduledClasses: ScheduledClassModel[];

  trackByFn(index: number, item: any) {
    return item.id;
  }

}
