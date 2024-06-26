import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Account } from '@app/_models';
import { System } from '@app/_models/system';
import { AccountService, AlertService, ProviderService } from '@app/_services';
import { SystemService } from '@app/_services/system.service';
import { first } from 'rxjs';

@Component({
  selector: 'app-systems',
  templateUrl: './systems.component.html',
})
export class SystemsComponent {
  systems?: System[];
  showScroll: boolean = false;
  isFetchingData: boolean = false;
  fetchingFrom: string = "";
  account?: Account | null;

  constructor(
    private systemService: SystemService,
    private providerService: ProviderService,
    private accountService: AccountService,
    private alertService: AlertService,
    private route: ActivatedRoute,
  ) {
    this.accountService.account.subscribe(x => this.account = x);
  }

  ngOnInit() {
    const pid = this.route.snapshot.params['pid'];
    if (pid) {
      this.providerService.getByPid(pid)
        .pipe(first())
        .subscribe(provider => {
          let providerSystems = provider["backends_ids"] ?? [];
          this.systemService.getAll()
            .pipe(first())
            .subscribe(systems => {
              this.systems = systems.filter(s => providerSystems.includes(s.id));
            });
        });
    } else {
      this.systemService.getAll()
        .pipe(first())
        .subscribe(systems => {
          console.log(systems);
          this.systems = systems.sort((a, b) =>
            this.compareSystems(a, b));
        });
    }
  }

  compareSystems(a: System, b: System) {
    let dateA = new Date(a.last_checked);
    let dateB = new Date(b.last_checked);
    let comparison = dateB.getTime() - dateA.getTime();
    return comparison;
  }

  updateSystem(system: System) {
    this.isFetchingData = true;
    this.fetchingFrom = system.provider.provider_from ?? system.provider.provider_id;
    this.systemService.refreshData({ "_id": system.provider.provider_id })
      .subscribe({
        next: () => {
          this.isFetchingData = false;
          for (let i = 3; i > 0; i--) {
            setTimeout(() => {
              this.alertService.clear();
              this.alertService.success(`
                <h4>System updated successfully</h4>
                <p>Page will reload in ${i}seg</p>
              `);
            }, (3 - i) * 1000);
          }
          setTimeout(() => {
            window.location.reload();
          }, 3000);
        },
        error: error => {
          console.log(error);
        }
      });
  }

}
