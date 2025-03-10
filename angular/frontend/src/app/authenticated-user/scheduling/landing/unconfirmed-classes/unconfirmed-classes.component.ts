import { Component, Input } from '@angular/core';

import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';

@Component({
  selector: 'app-unconfirmed-classes',
  standalone: false,
  templateUrl: './unconfirmed-classes.component.html',
  styleUrl: './unconfirmed-classes.component.css'
})
export class UnconfirmedClassesComponent {

  @Input() unconfirmedClasses: ScheduledClassModel[];

  trackByFn(index: number, item: any) {
    return item.id;
  }
}
