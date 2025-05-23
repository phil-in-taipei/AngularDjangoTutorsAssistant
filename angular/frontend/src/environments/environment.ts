// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  apiUrl: "http://localhost:8000",
  authTimerAmount: 590000, //(9 minutes and 50 seconds)
  tokenRefreshHoursAmount: 5,
  tokenRefreshMinsAmount: 59,
  tokenRefreshSecondsAmount: 51,
  tokenMinsAmount: 9,
  tokenSecondsAmount: 51,
  serial: "7b4e8f2c91d3a6h5g0j8k7l4m2n1p3q5r9s6t0u8v7w4x2y1z3A5B9C8D6E2F1G3H7I4J",
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.
