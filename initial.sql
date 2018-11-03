PostgreSQL is available
BEGIN;
--
-- Create model Beacon
--
CREATE TABLE "domain_beacon" ("id" serial NOT NULL PRIMARY KEY, "nombre" varchar(45) NOT NULL, "referencia" varchar(45) NOT NULL, "modelo" varchar(45) NOT NULL, "ubicacion" varchar(45) NOT NULL);
--
-- Create model Cliente
--
CREATE TABLE "domain_cliente" ("id" serial NOT NULL PRIMARY KEY, "correo" varchar(45) NOT NULL, "documento" varchar(45) NULL, "tipoDocumento" integer NOT NULL, "nombre" varchar(45) NOT NULL, "direccion" varchar(80) NOT NULL, "telefono" varchar(20) NOT NULL, "user_id" integer NOT NULL);
--
-- Create model Compra
--
CREATE TABLE "domain_compra" ("id" serial NOT NULL PRIMARY KEY, "cantidad" integer NOT NULL, "descuento" double precision NOT NULL, "medioPago" integer NOT NULL, "idCliente" integer NOT NULL);
--
-- Create model Interaccion
--
CREATE TABLE "domain_interaccion" ("id" serial NOT NULL PRIMARY KEY, "fecha" timestamp with time zone NOT NULL, "Materializado" boolean NOT NULL, "idCliente" integer NOT NULL);
--
-- Create model Notificacion
--
CREATE TABLE "domain_notificacion" ("id" serial NOT NULL PRIMARY KEY, "mensaje" varchar(100) NOT NULL, "idBeacon" integer NOT NULL);
--
-- Create model Producto
--
CREATE TABLE "domain_producto" ("id" serial NOT NULL PRIMARY KEY, "nombre" varchar(45) NOT NULL, "referencia" varchar(45) NOT NULL, "precio" double precision NOT NULL);
--
-- Create model TipoProducto
--
CREATE TABLE "domain_tipoproducto" ("id" serial NOT NULL PRIMARY KEY, "nombre" varchar(45) NOT NULL);
--
-- Add field tipoProducto to producto
--
ALTER TABLE "domain_producto" ADD COLUMN "idTipoProducto" integer NOT NULL;
--
-- Add field producto to notificacion
--
ALTER TABLE "domain_notificacion" ADD COLUMN "idProducto" integer NOT NULL;
--
-- Add field notificacion to interaccion
--
ALTER TABLE "domain_interaccion" ADD COLUMN "idNotificacion" integer NOT NULL;
--
-- Add field producto to compra
--
ALTER TABLE "domain_compra" ADD COLUMN "idProducto" integer NOT NULL;
ALTER TABLE "domain_cliente" ADD CONSTRAINT "domain_cliente_user_id_45445f4b_fk_users_user_id" FOREIGN KEY ("user_id") REFERENCES "users_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "domain_cliente_user_id_45445f4b" ON "domain_cliente" ("user_id");
ALTER TABLE "domain_compra" ADD CONSTRAINT "domain_compra_idCliente_aa949844_fk_domain_cliente_id" FOREIGN KEY ("idCliente") REFERENCES "domain_cliente" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "domain_compra_idCliente_aa949844" ON "domain_compra" ("idCliente");
ALTER TABLE "domain_interaccion" ADD CONSTRAINT "domain_interaccion_idCliente_424fdc31_fk_domain_cliente_id" FOREIGN KEY ("idCliente") REFERENCES "domain_cliente" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "domain_interaccion_idCliente_424fdc31" ON "domain_interaccion" ("idCliente");
ALTER TABLE "domain_notificacion" ADD CONSTRAINT "domain_notificacion_idBeacon_dbebc287_fk_domain_beacon_id" FOREIGN KEY ("idBeacon") REFERENCES "domain_beacon" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "domain_notificacion_idBeacon_dbebc287" ON "domain_notificacion" ("idBeacon");
CREATE INDEX "domain_producto_idTipoProducto_4d25d1d3" ON "domain_producto" ("idTipoProducto");
ALTER TABLE "domain_producto" ADD CONSTRAINT "domain_producto_idTipoProducto_4d25d1d3_fk_domain_ti" FOREIGN KEY ("idTipoProducto") REFERENCES "domain_tipoproducto" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "domain_notificacion_idProducto_66cd58e8" ON "domain_notificacion" ("idProducto");
ALTER TABLE "domain_notificacion" ADD CONSTRAINT "domain_notificacion_idProducto_66cd58e8_fk_domain_producto_id" FOREIGN KEY ("idProducto") REFERENCES "domain_producto" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "domain_interaccion_idNotificacion_957fdd9d" ON "domain_interaccion" ("idNotificacion");
ALTER TABLE "domain_interaccion" ADD CONSTRAINT "domain_interaccion_idNotificacion_957fdd9d_fk_domain_no" FOREIGN KEY ("idNotificacion") REFERENCES "domain_notificacion" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "domain_compra_idProducto_c5636b8c" ON "domain_compra" ("idProducto");
ALTER TABLE "domain_compra" ADD CONSTRAINT "domain_compra_idProducto_c5636b8c_fk_domain_producto_id" FOREIGN KEY ("idProducto") REFERENCES "domain_producto" ("id") DEFERRABLE INITIALLY DEFERRED;
COMMIT;
