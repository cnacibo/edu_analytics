const API_BASE_URL = process.env.REACT_APP_API_URL;

class ApiService {
    constructor() {
        this.base_url = API_BASE_URL;
    }

    async get(endpoint, params) {
        const url = new URL(`${this.base_url}/${endpoint}`)
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
        const response = await fetch(url, {
            method: 'GET',
            mode: 'cors',
            credentials: 'omit',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }
}

const api = new ApiService();

export const hseApi = {
    getPrograms: (params) => api.get('hse', params)
}

export const vuzopediaApi = {
    getPrograms: (params) => api.get('vuzopedia', params)
}
