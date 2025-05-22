--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Debian 17.5-1.pgdg120+1)
-- Dumped by pg_dump version 17.4

-- Started on 2025-05-14 15:27:02 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3391 (class 0 OID 16400)
-- Dependencies: 218
-- Data for Name: author; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.author ("authID", auth_name, auth_desc) FROM stdin;
A01	Shakespiere	writer
A02	Harmish	not writer
A03	Priyang	definitely not writer
\.


--
-- TOC entry 3395 (class 0 OID 16420)
-- Dependencies: 222
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.books ("BID", "authID", "pubID", "genreID", title, available) FROM stdin;
B100	A01	P01	G01	tmkoc	t
\.


--
-- TOC entry 3390 (class 0 OID 16395)
-- Dependencies: 217
-- Data for Name: borrower; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.borrower ("BorrowerID", "BID", borrower_name, borrower_date, return_date) FROM stdin;
00001	B100	Priyang	2020-01-15	2025-01-15
\.


--
-- TOC entry 3392 (class 0 OID 16405)
-- Dependencies: 219
-- Data for Name: genre; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.genre ("genreID", genre_name, genre_desc) FROM stdin;
G11	Rmantic	\N
G12	Thriller	So suspensetic
G01	Comedy	HAHA
\.


--
-- TOC entry 3394 (class 0 OID 16415)
-- Dependencies: 221
-- Data for Name: librarian; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.librarian ("librarianID", librarian_name, shift, hire_date) FROM stdin;
L01	Jethalal Gada	2024-05-01	\N
\.


--
-- TOC entry 3393 (class 0 OID 16410)
-- Dependencies: 220
-- Data for Name: publisher; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.publisher ("pubID", pub_name, pub_desc) FROM stdin;
P01	Tanna & co.	\N
P02	Bhimani publishers	publisher
\.


-- Completed on 2025-05-14 15:27:02 UTC

--
-- PostgreSQL database dump complete
--

