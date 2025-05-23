--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Debian 17.5-1.pgdg120+1)
-- Dumped by pg_dump version 17.4

-- Started on 2025-05-23 11:17:53 UTC

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 24577)
-- Name: author; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.author (
    "authID" character varying(5) NOT NULL,
    auth_name character varying(25) NOT NULL,
    auth_desc character varying(250)
);


ALTER TABLE public.author OWNER TO admin;

--
-- TOC entry 218 (class 1259 OID 24580)
-- Name: books; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.books (
    "BID" character varying(5) NOT NULL,
    "authID" character varying(5) NOT NULL,
    "pubID" character varying(5) NOT NULL,
    "genreID" character varying(5) NOT NULL,
    title character varying(100) NOT NULL,
    available boolean
);


ALTER TABLE public.books OWNER TO admin;

--
-- TOC entry 219 (class 1259 OID 24583)
-- Name: borrower; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.borrower (
    "BorrowerID" character varying(5) NOT NULL,
    "BID" character varying(5) NOT NULL,
    borrower_name character varying(25) NOT NULL,
    borrower_date date NOT NULL,
    return_date date NOT NULL
);


ALTER TABLE public.borrower OWNER TO admin;

--
-- TOC entry 220 (class 1259 OID 24586)
-- Name: genre; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.genre (
    "genreID" character varying(5) NOT NULL,
    genre_name character varying(15) NOT NULL,
    genre_desc character varying(250)
);


ALTER TABLE public.genre OWNER TO admin;

--
-- TOC entry 221 (class 1259 OID 24589)
-- Name: publisher; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.publisher (
    "pubID" character varying(5) NOT NULL,
    pub_name character varying(25) NOT NULL,
    pub_desc character varying(250)
);


ALTER TABLE public.publisher OWNER TO admin;

--
-- TOC entry 3226 (class 2606 OID 24593)
-- Name: author author_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.author
    ADD CONSTRAINT author_pkey PRIMARY KEY ("authID");


--
-- TOC entry 3228 (class 2606 OID 24595)
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY ("BID");


--
-- TOC entry 3230 (class 2606 OID 24597)
-- Name: borrower borrower_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.borrower
    ADD CONSTRAINT borrower_pkey PRIMARY KEY ("BorrowerID");


--
-- TOC entry 3232 (class 2606 OID 24599)
-- Name: genre genre_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY ("genreID");


--
-- TOC entry 3234 (class 2606 OID 24601)
-- Name: publisher publisher_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.publisher
    ADD CONSTRAINT publisher_pkey PRIMARY KEY ("pubID");


--
-- TOC entry 3235 (class 2606 OID 24602)
-- Name: books books_author; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_author FOREIGN KEY ("authID") REFERENCES public.author("authID") NOT VALID;


--
-- TOC entry 3236 (class 2606 OID 24607)
-- Name: books books_genre; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_genre FOREIGN KEY ("genreID") REFERENCES public.genre("genreID") NOT VALID;


--
-- TOC entry 3237 (class 2606 OID 24612)
-- Name: books books_publisher; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_publisher FOREIGN KEY ("pubID") REFERENCES public.publisher("pubID") NOT VALID;


--
-- TOC entry 3238 (class 2606 OID 24617)
-- Name: borrower borrower_books; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.borrower
    ADD CONSTRAINT borrower_books FOREIGN KEY ("BID") REFERENCES public.books("BID") NOT VALID;


-- Completed on 2025-05-23 11:17:53 UTC

--
-- PostgreSQL database dump complete
--

