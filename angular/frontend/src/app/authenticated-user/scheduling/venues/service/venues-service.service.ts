import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';

import { AuthService } from 'src/app/authentication/auth.service';
import { VenueSpaceModel } from 'src/app/models/venues.model';

@Injectable({
  providedIn: 'root'
})
export class VenuesServiceService {

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) { }

  // note: this  will only fetch tables for specific venues
  // that the teacher is a "member of" via a many-to-many relationship
  fetchAllVenueSpacesForTeacher(): Observable<VenueSpaceModel[]> {
    let token = this.authService.getAuthToken();
    return this.http.get<VenueSpaceModel[]>(
      `${environment.apiUrl}/api/venues/spaces/by-venue/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

}
