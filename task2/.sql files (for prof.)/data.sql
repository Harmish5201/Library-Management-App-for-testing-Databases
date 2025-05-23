--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Debian 17.5-1.pgdg120+1)
-- Dumped by pg_dump version 17.4

-- Started on 2025-05-23 12:34:22 UTC

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
-- TOC entry 3384 (class 0 OID 16389)
-- Dependencies: 217
-- Data for Name: author; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.author ("authID", auth_name, auth_desc) FROM stdin;
A01	Shakespiere	writer
A02	Harmish	not writer
A03	Priyang	definitely not writer
A04	Guido van Rossum	Inventor of Python programming language
A05	Miguel Grinberg	Known for Flask web development
A06	Agatha Christie	Renowned mystery writer
A07	J.K. Rowling	Author of the fantasy Harry Potter series
\.


--
-- TOC entry 3387 (class 0 OID 16398)
-- Dependencies: 220
-- Data for Name: genre; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.genre ("genreID", genre_name, genre_desc) FROM stdin;
G11	Rmantic	\N
G12	Thriller	So suspensetic
G01	Comedy	HAHA
G02	Drama	Serious narratives with emotional themes
G03	Technology	Books related to modern technology
G04	Education	Informative and instructional content
G05	Sci-Fi	Science fiction and futuristic tales
G06	Mystery	Whodunits and suspense thrillers
G07	Fantasy	Magical and otherworldly adventures
\.


--
-- TOC entry 3388 (class 0 OID 16401)
-- Dependencies: 221
-- Data for Name: publisher; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.publisher ("pubID", pub_name, pub_desc) FROM stdin;
P01	Tanna & co.	\N
P02	Bhimani publishers	publisher
P03	TechWorld	Focus on technology books
P04	EduBooks Ltd.	Educational content publisher
P05	WebDev Press	Specializes in web frameworks
P06	MysteryHouse	Thriller and crime stories
P07	FantasyWorks	Fantasy and magical tales
\.


--
-- TOC entry 3385 (class 0 OID 16392)
-- Dependencies: 218
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.books ("BID", "authID", "pubID", "genreID", title, available) FROM stdin;
B101	A02	P02	G02	Game of Codes	t
B102	A03	P03	G03	Linux Basics	t
B104	A05	P05	G04	Flask in Action	t
B105	A06	P06	G06	Murder on the Orient Express	t
B108	A02	P02	G02	Thrones and Codes	t
B109	A01	P01	G01	Gokuldham Diaries	t
B100	A01	P01	G01	tmkoc	t
B107	A03	P03	G03	Advanced Kernel Hacking	t
B106	A07	P07	G07	The Sorcerer Quest	t
B103	A04	P04	G04	Python Programming	t
\.


--
-- TOC entry 3386 (class 0 OID 16395)
-- Dependencies: 219
-- Data for Name: borrower; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.borrower ("BorrowerID", "BID", borrower_name, borrower_date, return_date) FROM stdin;
\.


-- Completed on 2025-05-23 12:34:22 UTC

--
-- PostgreSQL database dump complete
--

