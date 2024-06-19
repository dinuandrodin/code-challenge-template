-- public.weather_data definition

-- Drop table

-- DROP TABLE public.weather_data;

CREATE TABLE public.weather_data (
	id serial4 NOT NULL,
	station_id varchar(50) NOT NULL,
	"date" date NOT NULL,
	max_temp int4 NULL,
	min_temp int4 NULL,
	precipitation int4 NULL,
	CONSTRAINT weather_data_pkey PRIMARY KEY (id),
	CONSTRAINT weather_data_station_id_date_key UNIQUE (station_id, date)
);