import { useQuery } from "@tanstack/react-query";

import { getProducts } from "@/services/products/product.service";

export function useProducts(){
    return useQuery({
        queryKey: ["products"],
        queryFn: getProducts,
    })
}