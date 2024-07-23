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
  statusFilter: string = 'All';

  currentPage = 1;
  pageSize = 3;

  constructor(
    private providerService: ProviderService,
    private systemService: SystemService
  ) { }

  dataStructure: { provider: any, systems: any }[] = [];
  dataStructureFiltered: { provider: any, systems: any }[] = [];

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
        this.updateSystems(this.currentPage);

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
              let providerSystems = this.systems.filter(system => {
                return system.provider.provider_id === provider["id"];
              });
              dataStructure.push({ provider: minimalProvider, systems: providerSystems });
            });
            // filter out providers with no systems
            this.dataStructure = dataStructure.filter(elem => elem["systems"].length > 0);
            console.log(this.dataStructure);
            this.filterSystems();
          });
      });
  }

  updateSystems(currentPage: number) {
    this.subSystems = this.systems.slice(
      (currentPage - 1) * this.pageSize, currentPage * this.pageSize
    );
  }

  setSort(sort: string) {
    this.sort = sort;
    console.log(this.sort);
  }

  filterSystems(statusFilter: string = 'All') {
    let online = ["online", "running", "available"];
    let offline = ["offline", "calibrating", "reserved"];
    this.statusFilter = statusFilter;
    switch (statusFilter) {
      case 'All':
        this.dataStructureFiltered = this.dataStructure;
        break;
      case 'Online':
        this.dataStructureFiltered = this.dataStructure.map(provider => {
          return {
            provider: provider.provider,
            systems: provider.systems.filter(
              (system: System) => online.includes(system.status?.toLowerCase() ?? 'N/A')
            )
          }
        });
        this.dataStructureFiltered = this.dataStructureFiltered.filter(elem => elem["systems"].length > 0);
        break;
      case 'Offline':
        this.dataStructureFiltered = this.dataStructure.map(provider => {
          return {
            provider: provider.provider,
            systems: provider.systems.filter(
              (system: System) => offline.includes(system.status?.toLowerCase() ?? 'N/A')
            )
          }
        });
        this.dataStructureFiltered = this.dataStructureFiltered.filter(elem => elem["systems"].length > 0);
        break;
    }
    this.sortSystems(this.sort);
  }

  sortSystems(sort: string = 'Qubits') {
    this.sort = sort;
    switch (sort) {
      case 'Qubits':
        this.dataStructureFiltered = this.dataStructureFiltered.map(provider => {
          // ordenamos los sistemas de cada proveedor
          return {
            provider: provider.provider,
            systems: provider.systems.sort((a: System, b: System) => b.qubits! - a.qubits!)
          }
          // y luego ordenamos los proveedores
        }).sort((a, b) => b.systems[0].qubits! - a.systems[0].qubits!);
        break;
      case 'Queue':
        this.dataStructureFiltered = this.dataStructureFiltered.map(provider => {
          // ordenamos los sistemas de cada proveedor
          return {
            provider: provider.provider,
            systems: provider.systems.sort((a: System, b: System) => {
              return this.sortByQueue(a.queue, b.queue);
            })
          }
          // y luego ordenamos los proveedores
        }).sort((a, b) => {
          return this.sortByQueue(a.systems[0].queue, b.systems[0].queue);
        });
        break;
      case 'Price':
        this.dataStructureFiltered = this.dataStructureFiltered.map(provider => {
          // ordenamos los sistemas de cada proveedor
          return {
            provider: provider.provider,
            systems: provider.systems.sort((a: System, b: System) => {
              return this.sortByPrice(a.price, b.price);
            })
          }
          // y luego ordenamos los proveedores
        }).sort((a, b) => {
          return this.sortByPrice(a.systems[0].price, b.systems[0].price);
        });
        break;
    }
  }

  private toMilliseconds(formato: string): number {
    const diasRegex = /(\d+)d/;
    const horasRegex = /(\d+)hrs/;
    const minsRegex = /(\d+)min/;

    let dias = 0, horas = 0, mins = 0;

    const diasMatch = formato.match(diasRegex);
    if (diasMatch) {
      dias = parseInt(diasMatch[1]);
    }

    const horasMatch = formato.match(horasRegex);
    if (horasMatch) {
      horas = parseInt(horasMatch[1]);
    }

    const minsMatch = formato.match(minsRegex);
    if (minsMatch) {
      mins = parseInt(minsMatch[1]);
    }

    return ((dias * 24 * 60) + (horas * 60) + mins) * 60 * 1000;
  }

  private sortByQueue(aQueue: any, bQueue: any): number {
    if (aQueue === undefined && bQueue === undefined)
      return 0;
    else if (aQueue === undefined)
      return 1;
    else if (bQueue === undefined)
      return -1;

    let comparison = 0;
    if (aQueue.type === 'avg_time' && bQueue.type === 'avg_time') {
      comparison = this.toMilliseconds(aQueue.value) - this.toMilliseconds(bQueue.value);
    } else if (aQueue.type === 'jobs_remaining' && bQueue.type === 'jobs_remaining') {
      comparison = parseInt(aQueue.value) - parseInt(bQueue.value);
    }
    return comparison;
  }

  private sortByPrice(aPrice: any, bPrice: any): number {
    if (aPrice === undefined && bPrice === undefined)
      return 0;
    else if (aPrice === undefined)
      return 1;
    else if (bPrice === undefined)
      return -1;

    let comparison = 0;
    if (aPrice.per_shot_price !== undefined && bPrice.per_shot_price !== undefined) {
      comparison = aPrice.per_shot_price - bPrice.per_shot_price;
    } else if (aPrice.per_task_price !== undefined && bPrice.per_task_price !== undefined) {
      comparison = aPrice.per_task_price - bPrice.per_task_price;
    } else if (aPrice.per_minute_price !== undefined && bPrice.per_minute_price !== undefined) {
      comparison = aPrice.per_minute_price - bPrice.per_minute_price;
    }
    return comparison;
  }

}
