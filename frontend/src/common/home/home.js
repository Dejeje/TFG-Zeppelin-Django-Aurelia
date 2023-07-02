import { AuthService } from 'aurelia-authentication';
import { inject } from 'aurelia-framework';

@inject(AuthService)
export class Home {
    user = undefined;
    loading = true;

    constructor(authService) {
        this.authService = authService;

        this.authService.getMe()
            .then(profile => {
                this.user = profile;
                this.email = profile.email;
                setTimeout(() => this.loading = false, 1000);
            })
            .catch(err => {
                console.log("home failure " + err);
            });
    }
}
