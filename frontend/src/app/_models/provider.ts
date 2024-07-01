export class ThirdParty {
    third_party_id?: string;
    third_party_name?: string;
}

export class Description {
    short_description?: string;
    long_description?: string;
    history?: string;
}

export class Provider {
    id?: string;
    pid?: string;
    name?: string;
    description?: string | Description;
    website?: string;
    from_third_party?: boolean;
    fetchMethod?: string;
    third_party?: ThirdParty;
    backends_ids: string[];
    last_checked?: string;
    // To access the attributes of the object using a string key
    [key: string]: any;
}