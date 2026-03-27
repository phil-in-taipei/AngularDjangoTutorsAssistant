import { Component, OnInit, Input } from '@angular/core';
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
export class VenueSpaceTemplateStringComponent implements OnInit{

  venueSpace$: Observable<VenueSpaceModel | undefined> = of(undefined);
  @Input() venueSpaceId: number;

  ngOnInit(): void {
    this.venueSpace$ = this.store.pipe(select(
      selectVenueSpaceById(this.venueSpaceId)
    ));
  }

  constructor(
    private store: Store<VenuesSpacesState>
  ) {}

}
