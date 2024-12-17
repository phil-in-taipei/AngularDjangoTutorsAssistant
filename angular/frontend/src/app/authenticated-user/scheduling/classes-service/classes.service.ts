import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from 'src/environments/environment';
import { AuthService } from 'src/app/authentication/auth.service';
import { DeletionResponse } from 'src/app/models/deletion-response';
import { getDateString } from 'src/app/shared-utils/date-time.util';


@Injectable({
  providedIn: 'root'
})
export class ClassesService {

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) { }
}
