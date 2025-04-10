import { Component } from '@angular/core';
import { Observable, of } from 'rxjs';

@Component({
  selector: 'app-post-purchase-hours-update',
  standalone: false,
  templateUrl: './post-purchase-hours-update.component.html',
  styleUrl: './post-purchase-hours-update.component.css'
})
export class PostPurchaseHoursUpdateComponent {
  errMsg$: Observable<string | undefined> = of(undefined)
  successMsg$: Observable<string | undefined> = of(undefined)

}
