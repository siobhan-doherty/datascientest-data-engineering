--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8
-- Dumped by pg_dump version 16.8

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: audit_dog_update(); Type: FUNCTION; Schema: public; Owner: daniel
--

CREATE FUNCTION public.audit_dog_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	INSERT INTO DogsAudit ( DogId, DogName, BreedId, DogGender, DogTattooNumber, DogBirthDate, DogCoatColor, ClientId, SalePrice, SaleDate, ModificationDate ) 
	VALUES ( OLD.DogId, OLD.DogName, OLD.BreedId, OLD.DogGender, OLD.DogTattooNumber, OLD.DogBirthDate, OLD.DogCoatColor, OLD.ClientId, OLD.SalePrice, OLD.SaleDate, NOW() );
	RETURN NEW;
END;
$$;


ALTER FUNCTION public.audit_dog_update() OWNER TO daniel;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: breeds; Type: TABLE; Schema: public; Owner: daniel
--

CREATE TABLE public.breeds (
    breedid integer NOT NULL,
    breedname character varying(45) NOT NULL
);


ALTER TABLE public.breeds OWNER TO daniel;

--
-- Name: breeds_breedid_seq; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE public.breeds_breedid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.breeds_breedid_seq OWNER TO daniel;

--
-- Name: breeds_breedid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: daniel
--

ALTER SEQUENCE public.breeds_breedid_seq OWNED BY public.breeds.breedid;


--
-- Name: clients; Type: TABLE; Schema: public; Owner: daniel
--

CREATE TABLE public.clients (
    clientid integer NOT NULL,
    clientlastname character varying(45) NOT NULL,
    clientfirstname character varying(45) NOT NULL,
    clientaddress character varying(45) NOT NULL,
    clientpostalcode character varying(10) NOT NULL,
    clientcity character varying(60) NOT NULL,
    clientcountry character varying(45) NOT NULL,
    clientphone character varying(45) DEFAULT NULL::character varying,
    clientemail character varying(45) DEFAULT NULL::character varying
);


ALTER TABLE public.clients OWNER TO daniel;

--
-- Name: clients_clientid_seq; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE public.clients_clientid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clients_clientid_seq OWNER TO daniel;

--
-- Name: clients_clientid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: daniel
--

ALTER SEQUENCE public.clients_clientid_seq OWNED BY public.clients.clientid;


--
-- Name: dogs; Type: TABLE; Schema: public; Owner: daniel
--

CREATE TABLE public.dogs (
    dogid integer NOT NULL,
    dogname character varying(45) NOT NULL,
    breedid integer,
    doggender boolean,
    dogtattoonumber character varying(45) DEFAULT NULL::character varying,
    dogbirthdate date,
    dogcoatcolor character varying(45) DEFAULT NULL::character varying,
    clientid integer,
    saleprice numeric(10,0) DEFAULT NULL::numeric,
    saledate date
);


ALTER TABLE public.dogs OWNER TO daniel;

--
-- Name: dogs_dogid_seq; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE public.dogs_dogid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dogs_dogid_seq OWNER TO daniel;

--
-- Name: dogs_dogid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: daniel
--

ALTER SEQUENCE public.dogs_dogid_seq OWNED BY public.dogs.dogid;


--
-- Name: dogsaudit; Type: TABLE; Schema: public; Owner: daniel
--

CREATE TABLE public.dogsaudit (
    dogid integer NOT NULL,
    dogname character varying(45) NOT NULL,
    breedid integer,
    doggender boolean,
    dogtattoonumber character varying(45) DEFAULT NULL::character varying,
    dogbirthdate date,
    dogcoatcolor character varying(45) DEFAULT NULL::character varying,
    clientid integer,
    saleprice numeric(10,0) DEFAULT NULL::numeric,
    saledate date,
    modificationdate timestamp without time zone
);


ALTER TABLE public.dogsaudit OWNER TO daniel;

--
-- Name: dogsaudit_dogid_seq; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE public.dogsaudit_dogid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dogsaudit_dogid_seq OWNER TO daniel;

--
-- Name: dogsaudit_dogid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: daniel
--

ALTER SEQUENCE public.dogsaudit_dogid_seq OWNED BY public.dogsaudit.dogid;


--
-- Name: viewsdogssoldin2023; Type: VIEW; Schema: public; Owner: daniel
--

CREATE VIEW public.viewsdogssoldin2023 AS
 SELECT dogname,
    saledate,
    saleprice
   FROM public.dogs
  WHERE ((saledate >= '2023-01-01'::date) AND (saledate <= '2023-12-31'::date));


ALTER VIEW public.viewsdogssoldin2023 OWNER TO daniel;

--
-- Name: breeds breedid; Type: DEFAULT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY public.breeds ALTER COLUMN breedid SET DEFAULT nextval('public.breeds_breedid_seq'::regclass);


--
-- Name: clients clientid; Type: DEFAULT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY public.clients ALTER COLUMN clientid SET DEFAULT nextval('public.clients_clientid_seq'::regclass);


--
-- Name: dogs dogid; Type: DEFAULT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY public.dogs ALTER COLUMN dogid SET DEFAULT nextval('public.dogs_dogid_seq'::regclass);


--
-- Name: dogsaudit dogid; Type: DEFAULT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY public.dogsaudit ALTER COLUMN dogid SET DEFAULT nextval('public.dogsaudit_dogid_seq'::regclass);


--
-- Data for Name: breeds; Type: TABLE DATA; Schema: public; Owner: daniel
--

COPY public.breeds (breedid, breedname) FROM stdin;
1	Pitbull
2	Rottweiler
3	Chihuahua
4	Labrador
5	Dalmatian
6	Husky
7	Yorkshire
8	Poodle
9	Fox Terrier
10	Boxer
\.


--
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: daniel
--

COPY public.clients (clientid, clientlastname, clientfirstname, clientaddress, clientpostalcode, clientcity, clientcountry, clientphone, clientemail) FROM stdin;
1	Moreau	Anne	9 Rue du Cleps	31000	Toulouse	France	0616273216	anne.moreau@orange.fr
2	Mitchell	Eddy	97 Rue de Paris	75020	Paris	France	0158444288	e.mitchell@hotmail.fr
3	Moreau	William	33 Rue de Crimée	75020	Paris	France	0163243007	william.moreau@free.fr
4	Moreau	Lucia	20 Rue de la soif	75010	Paris	France	0142613306	lucia.moreau@orange.fr
5	Johnson	Céline	52 Rue du sac à dos	69008	Lyon	France	0618490352	celine.johnson@gmail.com
6	Thomas	Nathalie	76 Boulevard des Rousses	69002	Lyon	France 	0748072289	jean.martin@gmail.com
7	Martin	Nathalie	102 Avenue Phoque	70010	Paris	France	0176091014	emilie.moreau@free.fr
8	Gonzalez	Anne	49 Avenue de la joie	06118	Nice	France	0703825524	anne.gonzalez@hotmail.fr
9	Hernandez	José	26 rue Chivas	58010	Donzy	France	0713522885	j.hernandez@gmail.com
10	Hernandez	Samuel	15 rue des Violettes	75020	Paris	France	0167531477	youyou@hotmail.fr
11	Rorbert	Sophia	43 Rue Désirée	69025	Lyon	France	0608507445	sophia.robert@gmail.com
12	Hernandez	José	26 rue de la Modération	58010	Donzy	France	0614523296	j.hernandez2@gmail.com
13	Drier	Vincent	10 impasse des Pigeons	58000	Mesvre	France	\N	\N
14	Drier	Vincent	10 impasse des Pigeons	58000	Mesvre	France	\N	\N
\.


--
-- Data for Name: dogs; Type: TABLE DATA; Schema: public; Owner: daniel
--

COPY public.dogs (dogid, dogname, breedid, doggender, dogtattoonumber, dogbirthdate, dogcoatcolor, clientid, saleprice, saledate) FROM stdin;
2	Mentalo	6	f	\N	2017-09-15	White	2	966	2023-10-25
3	Maggie	6	t	99279	2014-03-27	Brown	3	883	2022-06-27
4	Whisky	2	t	35941	2020-03-11	Golden	4	543	2023-02-05
5	Bibi	6	t	88123	2020-10-10	Beige	\N	894	\N
6	Buddy	4	t	\N	2019-02-05	Red	5	250	2020-01-01
7	Sophie	5	f	\N	2016-07-01	Golden	5	644	2022-03-30
8	Molly	2	f	38281	2018-06-16	Gray	\N	\N	\N
9	Padbol	7	f	\N	2014-02-27	White and Black	\N	685	\N
10	Buddy	4	t	\N	2019-02-05	Red	6	847	2023-08-14
11	Bibi	8	f	61006	2018-06-30	Black	7	692	2022-09-28
12	Bibi	8	f	705423	2010-04-15	White	8	197	2021-02-22
13	Whisky	8	t	\N	2019-09-25	Beige	\N	\N	\N
14	Rocky	3	t	\N	2019-06-15	Black	\N	\N	\N
15	Whisky	6	t	\N	2018-09-02	Gray	9	449	2022-07-28
16	Duke	2	t	\N	2019-06-13	Black and White	10	300	2020-01-13
17	Buddy	5	t	\N	2015-02-13	Brown	11	410	2023-09-17
18	Lucy	9	f	56352	2019-10-01	Brown	3	363	2022-03-14
19	Whisky	10	t	\N	2017-08-03	Black	12	484	2023-12-01
20	Dora	5	f	25536	2023-07-01	White	5	1000	2022-03-30
21	Shrek	1	t	\N	2018-09-02	Green	12	250	2022-07-28
1	Wouf	5	t	55260	2021-09-24	White	1	999	2023-08-25
\.


--
-- Data for Name: dogsaudit; Type: TABLE DATA; Schema: public; Owner: daniel
--

COPY public.dogsaudit (dogid, dogname, breedid, doggender, dogtattoonumber, dogbirthdate, dogcoatcolor, clientid, saleprice, saledate, modificationdate) FROM stdin;
1	Wouf	5	t	55260	2021-09-24	White	1	980	2023-08-25	2025-05-09 11:31:10.491897
\.


--
-- Name: breeds_breedid_seq; Type: SEQUENCE SET; Schema: public; Owner: daniel
--

SELECT pg_catalog.setval('public.breeds_breedid_seq', 10, true);


--
-- Name: clients_clientid_seq; Type: SEQUENCE SET; Schema: public; Owner: daniel
--

SELECT pg_catalog.setval('public.clients_clientid_seq', 14, true);


--
-- Name: dogs_dogid_seq; Type: SEQUENCE SET; Schema: public; Owner: daniel
--

SELECT pg_catalog.setval('public.dogs_dogid_seq', 22, true);


--
-- Name: dogsaudit_dogid_seq; Type: SEQUENCE SET; Schema: public; Owner: daniel
--

SELECT pg_catalog.setval('public.dogsaudit_dogid_seq', 1, false);


--
-- Name: breeds breeds_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY public.breeds
    ADD CONSTRAINT breeds_pkey PRIMARY KEY (breedid);


--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (clientid);


--
-- Name: dogs dogs_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY public.dogs
    ADD CONSTRAINT dogs_pkey PRIMARY KEY (dogid);


--
-- Name: dogsaudit dogsaudit_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY public.dogsaudit
    ADD CONSTRAINT dogsaudit_pkey PRIMARY KEY (dogid);


--
-- Name: dogs before_update_dog; Type: TRIGGER; Schema: public; Owner: daniel
--

CREATE TRIGGER before_update_dog BEFORE UPDATE ON public.dogs FOR EACH ROW EXECUTE FUNCTION public.audit_dog_update();


--
-- Name: FUNCTION audit_dog_update(); Type: ACL; Schema: public; Owner: daniel
--

GRANT ALL ON FUNCTION public.audit_dog_update() TO antoine;
GRANT ALL ON FUNCTION public.audit_dog_update() TO data_engineer;


--
-- Name: TABLE breeds; Type: ACL; Schema: public; Owner: daniel
--

GRANT ALL ON TABLE public.breeds TO antoine;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.breeds TO data_engineer;


--
-- Name: SEQUENCE breeds_breedid_seq; Type: ACL; Schema: public; Owner: daniel
--

GRANT ALL ON SEQUENCE public.breeds_breedid_seq TO antoine;
GRANT ALL ON SEQUENCE public.breeds_breedid_seq TO data_engineer;


--
-- Name: TABLE clients; Type: ACL; Schema: public; Owner: daniel
--

GRANT ALL ON TABLE public.clients TO antoine;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.clients TO data_engineer;


--
-- Name: SEQUENCE clients_clientid_seq; Type: ACL; Schema: public; Owner: daniel
--

GRANT ALL ON SEQUENCE public.clients_clientid_seq TO antoine;
GRANT ALL ON SEQUENCE public.clients_clientid_seq TO data_engineer;


--
-- Name: TABLE dogs; Type: ACL; Schema: public; Owner: daniel
--

GRANT ALL ON TABLE public.dogs TO antoine;
GRANT SELECT ON TABLE public.dogs TO data_analyst;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.dogs TO data_engineer;


--
-- Name: SEQUENCE dogs_dogid_seq; Type: ACL; Schema: public; Owner: daniel
--

GRANT ALL ON SEQUENCE public.dogs_dogid_seq TO antoine;
GRANT ALL ON SEQUENCE public.dogs_dogid_seq TO data_engineer;


--
-- Name: TABLE dogsaudit; Type: ACL; Schema: public; Owner: daniel
--

GRANT ALL ON TABLE public.dogsaudit TO antoine;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.dogsaudit TO data_engineer;


--
-- Name: SEQUENCE dogsaudit_dogid_seq; Type: ACL; Schema: public; Owner: daniel
--

GRANT ALL ON SEQUENCE public.dogsaudit_dogid_seq TO antoine;
GRANT ALL ON SEQUENCE public.dogsaudit_dogid_seq TO data_engineer;


--
-- Name: TABLE viewsdogssoldin2023; Type: ACL; Schema: public; Owner: daniel
--

GRANT ALL ON TABLE public.viewsdogssoldin2023 TO antoine;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.viewsdogssoldin2023 TO data_engineer;


--
-- PostgreSQL database dump complete
--

