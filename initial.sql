BEGIN;
--
-- Create model User
--
CREATE TABLE "users_user" ("id" serial NOT NULL PRIMARY KEY, "password" varchar(128) NOT NULL, "last_login" timestamp with time zone NULL, "is_superuser" boolean NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(30) NOT NULL, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" boolean NOT NULL, "is_active" boolean NOT NULL, "date_joined" timestamp with time zone NOT NULL, "name" varchar(255) NOT NULL);
CREATE TABLE "users_user_groups" ("id" serial NOT NULL PRIMARY KEY, "user_id" integer NOT NULL, "group_id" integer NOT NULL);
CREATE TABLE "users_user_user_permissions" ("id" serial NOT NULL PRIMARY KEY, "user_id" integer NOT NULL, "permission_id" integer NOT NULL);
CREATE INDEX "users_user_username_06e46fe6_like" ON "users_user" ("username" varchar_pattern_ops);
ALTER TABLE "users_user_groups" ADD CONSTRAINT "users_user_groups_user_id_5f6f5a90_fk_users_user_id" FOREIGN KEY ("user_id") REFERENCES "users_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "users_user_groups" ADD CONSTRAINT "users_user_groups_group_id_9afc8d0e_fk_auth_group_id" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "users_user_groups" ADD CONSTRAINT users_user_groups_user_id_group_id_b88eab82_uniq UNIQUE ("user_id", "group_id");
CREATE INDEX "users_user_groups_user_id_5f6f5a90" ON "users_user_groups" ("user_id");
CREATE INDEX "users_user_groups_group_id_9afc8d0e" ON "users_user_groups" ("group_id");
ALTER TABLE "users_user_user_permissions" ADD CONSTRAINT "users_user_user_permissions_user_id_20aca447_fk_users_user_id" FOREIGN KEY ("user_id") REFERENCES "users_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "users_user_user_permissions" ADD CONSTRAINT "users_user_user_perm_permission_id_0b93982e_fk_auth_perm" FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "users_user_user_permissions" ADD CONSTRAINT users_user_user_permissions_user_id_permission_id_43338c45_uniq UNIQUE ("user_id", "permission_id");
CREATE INDEX "users_user_user_permissions_user_id_20aca447" ON "users_user_user_permissions" ("user_id");
CREATE INDEX "users_user_user_permissions_permission_id_0b93982e" ON "users_user_user_permissions" ("permission_id");
COMMIT;


BEGIN;
--
-- Create model Beacon
--
CREATE TABLE "beacon" ("id" serial NOT NULL PRIMARY KEY, "nombre" varchar(45) NOT NULL, "referencia" varchar(45) NOT NULL, "modelo" varchar(45) NOT NULL, "ubicacion" varchar(45) NOT NULL);
--
-- Create model Cliente
--
CREATE TABLE "cliente" ("id" serial NOT NULL PRIMARY KEY, "correo" varchar(45) NOT NULL, "documento" varchar(45) NULL, "tipoDocumento" integer NOT NULL, "nombre" varchar(45) NOT NULL, "direccion" varchar(80) NOT NULL, "telefono" varchar(20) NOT NULL, "user_id" integer NOT NULL);
--
-- Create model Compra
--
CREATE TABLE "compra" ("id" serial NOT NULL PRIMARY KEY, "cantidad" integer NOT NULL, "descuento" double precision NOT NULL, "medioPago" integer NOT NULL, "idCliente" integer NOT NULL);
--
-- Create model Interaccion
--
CREATE TABLE "interaccion" ("id" serial NOT NULL PRIMARY KEY, "fecha" timestamp with time zone NOT NULL, "Materializado" boolean NOT NULL, "idCliente" integer NOT NULL);
--
-- Create model Notificacion
--
CREATE TABLE "notificacion" ("id" serial NOT NULL PRIMARY KEY, "mensaje" varchar(100) NOT NULL, "idBeacon" integer NOT NULL);
--
-- Create model Producto
--
CREATE TABLE "producto" ("id" serial NOT NULL PRIMARY KEY, "nombre" varchar(45) NOT NULL, "referencia" varchar(45) NOT NULL, "precio" double precision NOT NULL);
--
-- Create model TipoProducto
--
CREATE TABLE "tipo_producto" ("id" serial NOT NULL PRIMARY KEY, "nombre" varchar(45) NOT NULL);
--
-- Add field tipoProducto to producto
--
ALTER TABLE "producto" ADD COLUMN "idTipoProducto" integer NOT NULL;
--
-- Add field producto to notificacion
--
ALTER TABLE "notificacion" ADD COLUMN "idProducto" integer NOT NULL;
--
-- Add field notificacion to interaccion
--
ALTER TABLE "interaccion" ADD COLUMN "idNotificacion" integer NOT NULL;
--
-- Add field producto to compra
--
ALTER TABLE "compra" ADD COLUMN "idProducto" integer NOT NULL;
ALTER TABLE "cliente" ADD CONSTRAINT "cliente_user_id_e7dabcb3_fk_users_user_id" FOREIGN KEY ("user_id") REFERENCES "users_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "cliente_user_id_e7dabcb3" ON "cliente" ("user_id");
ALTER TABLE "compra" ADD CONSTRAINT "compra_idCliente_591711be_fk_cliente_id" FOREIGN KEY ("idCliente") REFERENCES "cliente" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "compra_idCliente_591711be" ON "compra" ("idCliente");
ALTER TABLE "interaccion" ADD CONSTRAINT "interaccion_idCliente_5d577504_fk_cliente_id" FOREIGN KEY ("idCliente") REFERENCES "cliente" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "interaccion_idCliente_5d577504" ON "interaccion" ("idCliente");
ALTER TABLE "notificacion" ADD CONSTRAINT "notificacion_idBeacon_c3a030a3_fk_beacon_id" FOREIGN KEY ("idBeacon") REFERENCES "beacon" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "notificacion_idBeacon_c3a030a3" ON "notificacion" ("idBeacon");
CREATE INDEX "producto_idTipoProducto_646c70a8" ON "producto" ("idTipoProducto");
ALTER TABLE "producto" ADD CONSTRAINT "producto_idTipoProducto_646c70a8_fk_tipo_producto_id" FOREIGN KEY ("idTipoProducto") REFERENCES "tipo_producto" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "notificacion_idProducto_355b0d94" ON "notificacion" ("idProducto");
ALTER TABLE "notificacion" ADD CONSTRAINT "notificacion_idProducto_355b0d94_fk_producto_id" FOREIGN KEY ("idProducto") REFERENCES "producto" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "interaccion_idNotificacion_2e91d117" ON "interaccion" ("idNotificacion");
ALTER TABLE "interaccion" ADD CONSTRAINT "interaccion_idNotificacion_2e91d117_fk_notificacion_id" FOREIGN KEY ("idNotificacion") REFERENCES "notificacion" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "compra_idProducto_caab8f97" ON "compra" ("idProducto");
ALTER TABLE "compra" ADD CONSTRAINT "compra_idProducto_caab8f97_fk_producto_id" FOREIGN KEY ("idProducto") REFERENCES "producto" ("id") DEFERRABLE INITIALLY DEFERRED;
COMMIT;
