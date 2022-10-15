from src.domain.product.product import Product, ProductCreateOut, ProductUpdateOut
from src.infrastructure.adapters.output.repositories.entities import ProductEntity


class ProductMapper:

    @staticmethod
    def entity_to_domain(product: ProductEntity) -> Product:
        if not product:
            return product
        return Product(
            id=product.id,
            name=product.name,
            stock=product.stock,
            price=product.price,
            pvp=product.pvp,
            has_discount=product.has_discount,
            # category=Category.from_orm(product.category)
        )


class ProductCreateOutMapper:
    @staticmethod
    def entity_to_domain(product: ProductEntity) -> ProductCreateOut:
        if not product:
            return product
        return ProductCreateOut(
            id=product.id,
            name=product.name,
            stock=product.stock,
            price=product.price,
            pvp=product.pvp,
            has_discount=product.has_discount,
            category_id=product.category_id
        )


class ProductUpdateOutMapper:
    @staticmethod
    def entity_to_domain(product: ProductEntity) -> ProductUpdateOut:
        if not product:
            return product
        return ProductUpdateOut(
            id=product.id,
            name=product.name,
            stock=product.stock,
            price=product.price,
            pvp=product.pvp,
            has_discount=product.has_discount,
            category_id=product.category_id
        )
