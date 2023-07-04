import { PLATFORM } from 'aurelia-pal';
import authConfig from './auth/auth-config';

export function configure(aurelia) {
  aurelia.use
    .standardConfiguration()
    .developmentLogging()
    /* configure aurelia-authentication */
    .plugin(PLATFORM.moduleName('aurelia-authentication'), baseConfig => {
      baseConfig.configure(authConfig);
    });

  aurelia.use.plugin(PLATFORM.moduleName('aurelia-router'));

  aurelia.start().then(() => aurelia.setRoot(PLATFORM.moduleName('app')));
}
