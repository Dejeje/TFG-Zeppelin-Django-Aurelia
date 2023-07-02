import { AuthService } from 'aurelia-authentication';
import { inject, computedFrom } from 'aurelia-framework';
import { Router } from 'aurelia-router';

@inject(AuthService, Router)
export class Login {
    router;

    constructor(authService, router) {
        this.authService = authService;
        this.router = router;
    }

    email = '';
    password = '';

    login() {
        return this.authService.login(this.email, this.password)
            .then(response => {
                localStorage.setItem('access_token', response.access_token);   
            })
            .catch(err => {
                if(err.status == 400){
                    this.signupError = 'Introduce el correo correctamente';
                }
                else {
                    
                }// TODO RESPUESTA
                
                console.log("login failure: " + err.statusText);
                err.json()
                    .then(body => {
                        alert(`Error: ${body.detail}`);
            })
        });
    };
}