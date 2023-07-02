import {bindable} from 'aurelia-framework';
import {inject} from 'aurelia-framework';
import {AuthService} from 'aurelia-authentication';
import { Router } from 'aurelia-router';

@inject(AuthService, Router)
export class NavBar {
  // User isn't authenticated by default
  //_isAuthenticated = true;

  constructor(authService, router) {
    this.authService = authService;
    this.router = router;
  };

  // We can check if the user is authenticated
  // to conditionally hide or show nav bar items
  get isAuthenticated() {
    return this.authService.isAuthenticated();
  };

  logout(){
    localStorage.removeItem('access_token');
    this.authService.logout()
      .then(() => { 
        window.location.reload();
      });
  }
}