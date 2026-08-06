import api from "@/lib/axios";

export async funcion testConnection(){
    const response = await api.get("/products/");
    return response.data;
}