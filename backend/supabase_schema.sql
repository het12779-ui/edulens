-- EduLens Database Schema
-- Run this in Supabase SQL Editor before using the app

create table if not exists content (
  id uuid primary key,
  user_id uuid references auth.users(id),
  filename text not null,
  source_type text check (source_type in ('pdf','video','youtube')) not null,
  status text check (status in ('queued','processing','ready','failed')) default 'queued',
  transcript_preview text,
  created_at timestamptz default now()
);

create table if not exists outline_items (
  id uuid primary key default gen_random_uuid(),
  content_id uuid references content(id) on delete cascade,
  title text not null,
  summary text,
  timestamp_seconds numeric,
  page_number int,
  position int
);

create table if not exists flashcards (
  id uuid primary key default gen_random_uuid(),
  content_id uuid references content(id) on delete cascade,
  term text not null,
  definition text not null,
  source_ref text
);

create table if not exists chat_history (
  id uuid primary key default gen_random_uuid(),
  content_id uuid references content(id) on delete cascade,
  question text not null,
  answer text not null,
  created_at timestamptz default now()
);

-- Flexible jsonb columns for pipeline results
alter table content add column if not exists outline jsonb;
alter table content add column if not exists flashcards jsonb;
alter table content add column if not exists graph jsonb;
alter table content add column if not exists error text;