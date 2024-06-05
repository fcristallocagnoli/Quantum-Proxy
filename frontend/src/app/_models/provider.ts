export class ThirdParty {
    id?: string;
    name?: string;
}

export class Provider {
    id?: string;
    pid?: string;
    name?: string;
    description?: string;
    website?: string;
    fromThirdParty?: boolean;
    thirdParty?: ThirdParty;
}