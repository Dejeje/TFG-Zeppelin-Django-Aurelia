import 'bootstrap';
import { inject } from 'aurelia-framework';
import { Router } from 'aurelia-router';
import { AuthenticateStep, FetchConfig } from 'aurelia-authentication';

@inject(Router, FetchConfig)
export class App {
  constructor(router, fetchConfig) {
    this.router = router;
    this.fetchConfig = fetchConfig;
  }

  configureRouter(config) {

    config.title = 'ZeppelinUM';

    // this will add the interceptor for the Authorization header to the HttpClient singleton
    this.fetchConfig.configure();

    // Here we hook into the authorize extensibility point
    // to add a route filter so that we can require authentication
    // on certain routes
    config.addPipelineStep('authorize', AuthenticateStep);

    // Here we describe the routes we want along with information about them
    // such as which they are accessible at, which module they use, and whether
    // they should be placed in the navigation bar
    config.map([
      { route: ['', 'index'], name: 'index', moduleId: PLATFORM.moduleName('common/index/index'), nav: true, title: 'Index' },
      { route: 'registro', name: 'registro', moduleId: PLATFORM.moduleName('auth/registro/registro'), nav: false, title: 'Registro', authRoute: false },
      { route: 'login', name: 'login', moduleId: PLATFORM.moduleName('auth/login/login'), nav: false, title: 'Login', authRoute: true, auth: false },
      { route: 'home', name: 'home', moduleId: PLATFORM.moduleName('common/home/home'), nav: true, title: 'Home', auth: true },
      { route: 'platos', name: 'platos', moduleId: PLATFORM.moduleName('common/platos/platos'), nav: true, title: 'Platos', auth: true },
      { route: 'plato-detail', name: 'plato-detail', moduleId: PLATFORM.moduleName('common/plato-detail/plato-detail'), nav: true, title: 'Detalle Plato', auth: true },
      { route: 'restaurante-detail', name: 'restaurante-detail', moduleId: PLATFORM.moduleName('common/restaurante-detail/restaurante-detail'), nav: true, title: 'Detalle Restaurant', auth: true },
      { route: 'validate-users', name: 'validate-users', moduleId: PLATFORM.moduleName('common/usuarios/validar'), nav: true, title: 'Validar Usuarios', auth: true }
    ]);
  };
}
