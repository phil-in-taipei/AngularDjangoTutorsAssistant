import { Component, OnInit } from '@angular/core';
//import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from './authentication/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'frontend';


  constructor(private authService: AuthService) {}

  ngOnInit() {
    console.log("****main app component initializing and calling autoAuthUser function*****");
    this.authService.autoAuthUser();
  }
}
