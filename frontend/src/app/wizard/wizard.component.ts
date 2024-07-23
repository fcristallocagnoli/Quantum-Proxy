import { Component, OnInit } from '@angular/core';
import { Provider, System } from '@app/_models';
import { ProviderService, SystemService } from '@app/_services';
import { first } from 'rxjs';

@Component({
  templateUrl: './wizard.component.html',
})
export class WizardComponent implements OnInit {
  systems: System[];
  subSystems: System[];

  sort: string = 'Qubits';
  statusSort: string = 'All';

  page = 1;
  pageSize = 3;

  constructor(
    private providerService: ProviderService,
    private systemService: SystemService
  ) { }

  dataStructure: { provider: any, systems: any }[] = [];

  // TODO: Remoce in next commit
  // machines = [
  //   {
  //     name: 'IBM Quantum Experience',
  //     description: 'Explore the power of quantum computing with IBM\'s cloud-based platform.',
  //     qubits: 65,
  //     queueTime: '5 mins',
  //     price: '$0.10/shot',
  //     status: 'Available'
  //   },
  //   {
  //     name: 'Google Quantum Computing',
  //     description: 'Harness the power of quantum computing with Google\'s cloud-based platform.',
  //     qubits: 72,
  //     queueTime: '10 mins',
  //     price: '$0.15/shot',
  //     status: 'Available'
  //   },
  //   {
  //     name: 'Amazon Braket',
  //     description: 'Explore quantum computing with Amazon\'s cloud-based platform.',
  //     qubits: 60,
  //     queueTime: '15 mins',
  //     price: '$0.20/shot',
  //     status: 'Busy'
  //   }
  // ];

  ngOnInit() {
    let dataStructure: any[] = [];
    this.systemService.getAll()
      .pipe(first())
      .subscribe(systems => {
        this.systems = systems;
        this.updateSystems(this.page);

        this.providerService.getAll()
          .pipe(first())
          .subscribe(providers => {
            providers.forEach(provider => {
              let minimalProvider = {
                name: provider.name,
                pid: provider.pid,
                description: provider.description,
                website: provider.website,
                thirdParty: provider.third_party?.third_party_name,
                lastChecked: provider.last_checked
              }
              let providerSystems = this.systems.filter(system => system.provider.provider_id === provider["id"]);
              dataStructure.push({ provider: minimalProvider, systems: providerSystems });
            });
            // filter out providers with no systems
            this.dataStructure = dataStructure.filter(elem => elem["systems"].length > 0);
            console.log(this.dataStructure);
          });
      });
  }

  updateSystems(currentPage: number) {
    this.subSystems = this.systems.slice((currentPage - 1) * this.pageSize, currentPage * this.pageSize);
  }

  setSort(sort: string) {
    this.sort = sort;
    console.log(this.sort);
  }

}
