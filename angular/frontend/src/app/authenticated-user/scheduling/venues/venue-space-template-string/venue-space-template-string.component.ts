import { Component, Input, OnChanges, SimpleChanges } from '@angular/core'; //OnInit,
import { of, Observable } from 'rxjs';
import { select, Store } from '@ngrx/store';

import { VenueSpaceModel } from 'src/app/models/venues.model';
import { VenuesSpacesState } from '../state/venues.reducers';
import { selectVenueSpaceById } from '../state/venues.selectors';

@Component({
  selector: 'app-venue-space-template-string',
  standalone: false,
  templateUrl: './venue-space-template-string.component.html',
  styleUrl: './venue-space-template-string.component.css'
})
export class VenueSpaceTemplateStringComponent implements OnChanges {

  venueSpace$: Observable<VenueSpaceModel | undefined> = of(undefined);
  @Input() venueSpaceId: number;

  //ngOnInit(): void {
  //  this.venueSpace$ = this.store.pipe(select(
  //    selectVenueSpaceById(this.venueSpaceId)
  //  ));
  //}
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['venueSpaceId']) {
      this.venueSpace$ = this.store.pipe(select(
        selectVenueSpaceById(this.venueSpaceId)
      ));
    }
  }

  constructor(
    private store: Store<VenuesSpacesState>
  ) {}

}
