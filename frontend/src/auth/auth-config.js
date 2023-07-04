
export default {
  endpoint: null,
  configureEndpoints: null,

  // The SPA url to which the user is redirected after a successful login
  loginRedirect: '#/home',
  // The SPA url to which the user is redirected after a successful login
  signupRedirect: '#/login',
  // The SPA url to which the user is redirected after a successful logout
  logoutRedirect: '#/',
  // The SPA route used when an unauthenticated user tries to access an SPA page that requires authentication
  loginRoute: 'login',
  // Whether or not an authentication token is provided in the response to a successful signup
  loginOnSignup: false,
  // The SPA url to load when the token expires (null = don't redirect)
  expiredRedirect: '#/',
  // The SPA url to load when the authentication status changed in other tabs/windows (detected through storageEvents) (null = don't redirect)
  storageChangedRedirect: '#/',
  // API related options
  // ===================

  // The base url used for all authentication related requests, including provider.url below.
  // This appends to the httpClient/endpoint base url, it does not override it.
  baseUrl: 'http://localhost:8000',
  // The API endpoint to which login requests are sent
  loginUrl: 'zeppelin/usuario/login/',
  // The API endpoint to which logout requests are sent (not needed for jwt)
  logoutUrl: "zeppelin/usuario/logout/",
  // The HTTP method used for 'logout' requests (Options: 'get' or 'post')
  logoutMethod: 'get',
  // The API endpoint to which signup requests are sent
  signupUrl: 'zeppelin/usuario/',
  // The API endpoint used in profile requests (inc. `find/get` and `update`)
  profileUrl: 'zeppelin/usuario/perfil/',
  // The method used to update the profile ('put' or 'patch')
  //profileMethod : 'patch',


  // Configurar el encabezado personalizado para enviar el sessionid
  // Prefix to add before the token value in the Authorization header
  tokenPrefix: 'Token ',
  // Name of the header to send the token in
  authHeader: 'Authorization',
  // Name of the property in the server response that contains the token value
  responseTokenProp: 'localStorage.access_token',

  // Flag indicating whether to use a refresh token for authentication
  useRefreshToken: false,
  // Flag indicating whether to validate the authentication status on page load
  validateOnPageLoad: true,

// Token Options
// =============
// The header property used to contain the authToken in the header of API requests that require authentication
  // The token name used in the header of API requests that require authentication
  authTokenType: 'Token ',
  // The property from which to get the access token after a successful login or signup
  accessTokenProp: 'access_token',

  // Whether to enable the fetch interceptor which automatically adds the authentication headers
  // (or not... e.g. if using a session based API or you want to override the default behaviour)
  httpInterceptor : true,
  // For OAuth only: Tell the API whether or not to include token cookies in the response (for session based APIs)
  withCredentials : false,
  // Controls how the popup is shown for different devices (Options: 'browser' or 'mobile')
  platform : 'browser',
  // Determines the `window` property name upon which aurelia-authentication data is stored (Default: `window.localStorage`)
  storage : 'localStorage',
  // full page reload if authorization changed in another tab (recommended to set it to 'true')
  storageChangedReload : true,

  // Default headers for login and token-update endpoint
  defaultHeadersForTokenRequests: {
    'Content-Type': 'application/json',
  },
};