import { catchError, of, timeout } from 'rxjs';

import { AccountService, AlertService } from '@app/_services';

export function appInitializer(accountService: AccountService, alertService: AlertService) {
  return () => accountService.refreshToken()
    .pipe(timeout(5000)).pipe(
      // catch error to start app on success or failure
      catchError((error) => {
        alertService.warn(`
          <h4>Backend server is starting up...</h4>
          <p>It may take a few minutes for the backend server to start up and for the app to become fully functional.</p>
          <p>Please wait for a while and then refresh the page.</p>
        `, { autoClose: false, keepAfterRouteChange: true });
        console.log('Error refreshing token', error);
        return of();
      })
    );
}