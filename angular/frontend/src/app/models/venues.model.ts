export interface VenueBasicModel {
  id: number;
  venue_name: string;
}

export interface VenueSpaceModel {
  id: number;
  space_name: string;
  venue: VenueBasicModel;
  number_of_seats: number;
}
