import { inject } from '@angular/core';
import { Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

import { AccountService } from '@app/_services';

export function authGuard(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
  // router: Router, accountService: AccountService
  const router = inject(Router);
  const accountService = inject(AccountService);
  const account = accountService.accountValue;
  if (account) {
    // check if route is restricted by role
    if (route.data['roles'] && !route.data['roles'].includes(account.role)) {
      // role not authorized so redirect to home page
      router.navigate(['/']);
      return false;
    }

    // authorized so return true
    return true;
  }

  // not logged in so redirect to login page with the return url 
  // this.router.navigate(['/account/login'], { queryParams: { returnUrl: state.url } });
  router.navigate(['/account/login']);
  return false;
}