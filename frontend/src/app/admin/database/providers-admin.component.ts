import { Component, OnInit } from '@angular/core';
import { ConfirmationModal } from '@app/_components';
import { AlertService, ProviderService } from '@app/_services';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { first } from 'rxjs';

@Component({
  templateUrl: './providers-admin.component.html',
})
export class ProvidersAdminComponent implements OnInit {

  providers: any[];

  searchValue: string;

  constructor(
    private providerService: ProviderService,
    private alertService: AlertService,
    private modalService: NgbModal
  ) { }

  ngOnInit() {
    this.providerService.getAll()
      .pipe(first())
      .subscribe(providers => {
        this.providers = providers;
      });
  }

  filterProviders() {
    if (this.searchValue) {
      this.providers = this.providers.filter(provider => {
        return provider.name.toLowerCase().includes(this.searchValue.toLowerCase());
      });
    } else {
      this.providerService.getAll()
        .pipe(first())
        .subscribe(providers => {
          this.providers = providers;
        });
    }
  }

  deleteProvider(pid: string) {
    let ref = this.modalService.open(ConfirmationModal);
    ref.componentInstance.buildModal("deletion");
    ref.componentInstance.bodyText = "Are you sure that you want to delete this provider?";
    ref.result.then((result) => {
      if (result === 'ok click') {
        const provider = this.providers!.find(x => x.pid === pid);
        provider.isDeleting = true;
        this.providerService.deleteByPid(pid)
          .pipe(first())
          .subscribe({
            next: () => {
              this.providers = this.providers!.filter(x => x.pid !== pid)
              this.alertService.success('Provider deleted successfully', { autoClose: true });
            },
            error: error => {
              this.alertService.error(error);
            }
          });
      }
    });
  }

}
