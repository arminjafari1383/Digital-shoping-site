import api from "@/lib/axios";

export async function getProducts(){
    const response = await api.get("/products/");

    return response.data;
}