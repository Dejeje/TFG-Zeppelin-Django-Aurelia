import {inject} from 'aurelia-framework';
import {AuthService} from 'aurelia-authentication';
import { Router } from 'aurelia-router';

@inject(AuthService, Router)
export class NavBar {

  constructor(authService, router) {
    this.authService = authService;
    this.router = router;
  };

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