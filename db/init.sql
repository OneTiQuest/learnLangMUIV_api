-- public.courses определение

-- Drop table

-- DROP TABLE public.courses;

CREATE TABLE public.courses (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NULL,
	code varchar NULL,
	CONSTRAINT course_pk PRIMARY KEY (id)
);


-- public.exercise_type определение

-- Drop table

-- DROP TABLE public.exercise_type;

CREATE TABLE public.exercise_type (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NULL,
	CONSTRAINT exercise_type_pk PRIMARY KEY (id)
);


-- public.langs определение

-- Drop table

-- DROP TABLE public.langs;

CREATE TABLE public.langs (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NOT NULL,
	short_name varchar NULL,
	CONSTRAINT langs_pk PRIMARY KEY (id)
);


-- public.roles определение

-- Drop table

-- DROP TABLE public.roles;

CREATE TABLE public.roles (
	id int8 NOT NULL,
	"name" varchar NULL,
	CONSTRAINT roles_pk PRIMARY KEY (id)
);


-- public.settings определение

-- Drop table

-- DROP TABLE public.settings;

CREATE TABLE public.settings (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	settings varchar NULL,
	user_id int8 NOT NULL,
	CONSTRAINT settings_pk PRIMARY KEY (id)
);


-- public.modules определение

-- Drop table

-- DROP TABLE public.modules;

CREATE TABLE public.modules (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NULL,
	lang_id int8 NULL,
	CONSTRAINT modules_pk PRIMARY KEY (id),
	CONSTRAINT modules_langs_fk FOREIGN KEY (lang_id) REFERENCES public.langs(id)
);


-- public.themes определение

-- Drop table

-- DROP TABLE public.themes;

CREATE TABLE public.themes (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NULL,
	"order" int4 DEFAULT 0 NULL,
	module_id int8 NULL,
	CONSTRAINT themes_pk PRIMARY KEY (id),
	CONSTRAINT themes_modules_fk FOREIGN KEY (module_id) REFERENCES public.modules(id) ON DELETE CASCADE
);


-- public.users определение

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar NULL,
	last_name varchar NULL,
	login varchar NOT NULL,
	password varchar NOT NULL,
	chat_id int8 NULL,
	role_id int8 NULL,
	created_at date DEFAULT now() NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (id),
	CONSTRAINT users_roles_fk FOREIGN KEY (role_id) REFERENCES public.roles(id)
);
CREATE INDEX users_id_idx ON public.users USING btree (id);
CREATE INDEX users_chat_id_idx ON public.users USING btree (chat_id);


-- public.users_langs определение

-- Drop table

-- DROP TABLE public.users_langs;

CREATE TABLE public.users_langs (
	user_id int8 NULL,
	lang_id int8 NULL,
	CONSTRAINT users_langs_langs_fk FOREIGN KEY (lang_id) REFERENCES public.langs(id)
);


-- public.courses_modules определение

-- Drop table

-- DROP TABLE public.courses_modules;

CREATE TABLE public.courses_modules (
	course_id int8 NULL,
	module_id int8 NULL,
	CONSTRAINT courses_modules_courses_fk FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE,
	CONSTRAINT courses_modules_modules_fk FOREIGN KEY (module_id) REFERENCES public.modules(id) ON DELETE CASCADE
);


-- public.courses_modules определение

-- Drop table

-- DROP TABLE public.courses_modules;

CREATE TABLE public.courses_users (
	course_id int8 NULL,
	user_id int8 NULL,
	CONSTRAINT courses_users_courses_fk FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE,
	CONSTRAINT courses_users_users_fk FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE
);

-- public.exercise определение

-- Drop table

-- DROP TABLE public.exercise;

CREATE TABLE public.exercise (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	title varchar NULL,
	"order" int4 DEFAULT 0 NULL,
	another_data varchar NULL,
	theme_id int8 NULL,
	type_id int8 NULL,
	CONSTRAINT exercise_pk PRIMARY KEY (id),
	CONSTRAINT exercise_exercise_type_fk FOREIGN KEY (type_id) REFERENCES public.exercise_type(id),
	CONSTRAINT exercise_themes_fk FOREIGN KEY (theme_id) REFERENCES public.themes(id) ON DELETE CASCADE
);


-- public.grades определение

-- Drop table

-- DROP TABLE public.grades;

CREATE TABLE public.grades (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	user_id int8 NULL,
	theme_id int8 NULL,
	grade int4 NULL,
	CONSTRAINT grades_pk PRIMARY KEY (id),
	CONSTRAINT grades_themes_fk FOREIGN KEY (theme_id) REFERENCES public.themes(id) ON DELETE CASCADE
);


-- public.answers определение

-- Drop table

-- DROP TABLE public.answers;

CREATE TABLE public.answers (
	user_id int8 NOT NULL,
	exercise_id int8 NOT NULL,
	answer varchar NULL,
	CONSTRAINT answers_exercise_fk FOREIGN KEY (exercise_id) REFERENCES public.exercise(id)
);



/*
	Заполнение пользователей
*/
INSERT INTO public.roles (id,"name") VALUES
	 (1,'Ученик'),
	 (2,'Преподаватель'),
	 (3,'Администратор');

INSERT INTO public.users ("name",last_name,login,password,chat_id,role_id) VALUES
	 ('Администратор',NULL,'admin','21232f297a57a5a743894a0e4a801fc3', NULL,3);
	
-- INSERT INTO public.settings (settings,user_id) VALUES ();


/*
	Заполнение языков
*/
INSERT INTO public.langs (name,short_name) VALUES
	 ('Английский','🇬🇧'),
	 ('Французский','🇨🇵'),
	 ('Немецкий','🇩🇪');
	 
INSERT INTO public.users_langs (user_id,lang_id) VALUES
	 (1,2);


/*
	Заполнение курсов
*/
INSERT INTO public.courses (name,code) VALUES
	 ('Прикладная информатика','09.03.03'),
	 ('Психолого-педагогическое образование','44.03.02'),
	 ('Туризм ','43.03.02'),
	 ('Юриспруденция ','40.03.01'),
	 ('Бизнес-информатика','38.03.05'),
	 ('Государственное и муниципальное управление','38.03.04'),
	 ('Экономика ','38.03.01');


/*
	Заполнение модулей
*/
INSERT INTO public.modules (name,lang_id) VALUES
	 ('Pre-Intermediate (A2)',2),
	 ('Intermediate (B1)',2),
	 ('Upper-Intermediate (B2)',2),
	 ('Advanced (C1)',2),
	 ('Уровень А1 (Anfänger)',1),
	 ('Уровень А2 (Grundlagen)',1),
	 ('Уровень В1 (Aufbau 1)',1),
	 ('Уровень B2 (Aufbau 2)',1),
	 ('Уровень С1 (Fortgeschrittene 1)',1),
	 ('Уровень С2 (Fortgeschrittene 2)',1),
	 ('Модуль 1',3),
	 ('Модуль 2',3),
	 ('англ яз 2',2),
	 ('Beginer (A1)',2),
	 ('ba4',2),
	 ('у1',2),
	 ('Начальный1',3);


/*
	Заполнение тем
*/
INSERT INTO public.themes (name,"order",module_id) VALUES
	 ('Глагол to be',0,1),
	 ('Типы предложений',0,1),
	 ('Артикли',0,1),
	 ('Описательный оборот there is/are',0,1),
	 ('Предлоги времени',0,2),
	 ('Something/anything/nothing',0,2),
	 ('Глаголы состояния',0,3),
	 ('Модальные глаголы в прошедшем времени',0,5),
	 ('Условные предложения смешанного типа',0,5),
	 ('Обратный порядок слов в предложении',0,5),
	 ('Каузативные глаголы get/have',0,5),
	 ('Нулевой артикль',0,4),
	 ('Косвенные вопросы',0,4),
	 ('Порядок слов в вопросительных предложениях',0,2),
	 ('Притяжательные местоимения mine, his, hers, its, yours, ours, theirs',0,2),
	 ('Придаточные определительные предложения с that/who/which/where',0,3),
	 ('Модальные глаголы have to, must, should, may, might',0,3),
	 ('Предположения с модальными глаголами can’t, might, must',0,4),
	 ('Квантификаторы a little/little, a few/few, plenty of/a lot of, all, every, both, no/none, most',0,4),
	 ('Герундий',0,3),
	 ('Алфавит (Alphabet)',0,7),
	 ('Существительные и артикли (Nomen und Artikel)',0,7),
	 ('Личные местоимения (Personalpronomen)',0,7),
	 ('Глаголы: настоящее время (Verben: Präsens)',0,7),
	 ('Настоящее время (Präsens)',0,8),
	 ('Совершенное время (Perfekt)',0,8),
	 ('Сравнительные союзы (Vergleichssätze)',0,8),
	 ('Повелительное наклонение (Imperativ)',0,8),
	 ('Глаголы с предлогами (Verben mit Präpositionen)',0,9),
	 ('Условные предложения (Bedingungssätze)',0,9),
	 ('Прошедшее время (Perfekt, Präteritum)',0,9),
	 ('Косвенная речь (Indirekte Rede)',0,9),
	 ('Пассивный залог (Passiv)',0,10),
	 ('Относительные предложения (Relativsätze)',0,10),
	 ('Способы выражения будущего времени (Futurformen)',0,10),
	 ('Немецкие падежи (Nominativ, Genitiv, Dativ, Akkusativ)',0,10),
	 ('Герундий и инверсия (Gerundium und Inversion)',0,11),
	 ('Причастные конструкции (Die Partizipialkonstruktionen)',0,11),
	 ('Инфинитивные конструкции (Die Infinitivkonstruktionen)',0,11),
	 ('Различные виды придаточных предложений (Die verschiedenen Arten von Nebensätzen)',0,11),
	 ('Степени сравнения (Die Steigerungsformen)',0,12),
	 ('Различные виды сравнений (Komparationen)',0,12),
	 ('Сложные предлоги и союзы (Zusammengesetzte Präpositionen und Konjunktionen)',0,12),
	 ('Различные виды прямой речи (Indirekte Rede)',0,12);

INSERT INTO public.grades (user_id,theme_id,grade) VALUES
	 (1,18,2),
	 (1,4,2),
	 (1,2,2),
	 (1,3,2),
	 (1,21,2),
	 (1,1,3);


/*
	Заполнение упражнений
*/
INSERT INTO public.exercise_type (name) VALUES
	 ('Недостающее слово'),
	 ('Правильный вариант'),
	 ('Аудио'),
	 ('Теория');
	 
INSERT INTO public.exercise (title,"order",another_data,theme_id,type_id) VALUES
	 ('I ______ to the gym every Monday and Wednesday.',0,'{"answers": ["go", "am going", "goes", "have gone"], "success_answer": "am going"}',2,2),
	 ('You ______ finish your homework before you play video games.',0,'{"answers": ["must", "can", "would", "may"], "success_answer": "must"}',3,2),
	 ('She is ______ architect. She designs beautiful houses.',0,'{"answers": ["a", "an", "the"], "success_answer": "an"}',4,2),
	 ('Применение глагола',0,'{"content": [{"type": "text", "data": "Глагол to be играет важную роль в английской грамматике. Точнее сказать, роли: это и самостоятельный глагол, и вспомогательный, и глагол-связка. Без глагола to be не получится построить предложения в пассивном залоге и во временах группы Continuous. Кроме того, to be входит в состав некоторых конструкций и фразовых глаголов."}]}',1,4),
	 ('My birthday is ______ July.',0,'{"answers": ["in", "on", "at", "by"], "success_answer": "in"}',2,2),
	 ('Произношение глагола',1,'{"content": [{"type": "text", "data": "Глагол to be имеет разные формы произношения в зависимости от времени и лица: в настоящем времени это am [æm], is [ɪz] и are [ɑ:]; в прошедшем — was [wɒz] и were [wɜː]; а в прошедшем совершенном времени добавляется форма been [biːn]."}]}',1,4),
	 ('This is ______ movie I have ever seen!',0,'{"answers": ["the most exciting", "most exciting", "the excitest", "the more exciting"], "success_answer": "the most exciting"}',2,2),
	 ('This book isnt mine. Is it ______?',0,'{"success_answer": "the most exciting", "answers": ["your", "you", "yours"]}',3,2),
	 ('What ______ at 8 p.m. yesterday?',0,'{"answers": ["did you do", "were you doing", "are you doing", "have you done"], "success_answer": "were you doing"}',3,2),
	 ('If it ______ tomorrow, we will cancel the picnic.',0,'{"answers": ["rains", "will rain", "rained", "would rain"], "success_answer": "rains"}',4,2),
	 ('______ you our new teacher? ',3,'{"success_answer": "are"}',1,1),
	 ('I ____ a student.',4,'{"answers": ["am", "is", "have", "go"], "success_answer": "am"}',1,2),
	 ('Could you ______ the music? Its too loud.',0,'{"answers": ["turn down", "turn up", "turn on", "turn off"], "success_answer": "turn down"}',4,2),
	 ('Прослушайте запись',2,'{"path": "./media/audio/3.mp3"}',1,3),
	 ('We need to buy ______ for the recipe.',0,'{"answers": ["a bread", "some breads", "some bread", "a few bread"], "success_answer": "some bread"}',18,2),
	 ('He ______ in London since 2010.',0,'{"answers": ["has lived", "lived", "is living", "lives"], "success_answer": "has lived"}',18,2),
	 ('I ____ a dog',0,'{"answers": ["am", "da", "net"], "success_answer": "da"}',1,2),
	 ('The new bridge ______ last year.',0,'{"answers": ["is built", "was built", "built", "has been built"], "success_answer": "was built"}',18,2),
	 ('Choose the word that is closest in meaning to "BIG":',0,'{"answers": ["small", "large", "tiny", "little"], "success_answer": "large"}',NULL,2),
	 ('The keys are ______ the table.',0,'{"answers": ["in", "on", "at", "by"], "success_answer": "on"}',NULL,2),
	 ('He told me he ______ a doctor.',0,'{"answers": ["is", "was", "were", "has been"], "success_answer": "was"}',NULL,2),
	 ('Its raining ______. Dont forget your umbrella.',0,'{"answers": ["cats and dogs", "fish and frogs", "buckets", "water and ice"], "success_answer": "cats and dogs"}',NULL,2),
	 ('Im not used to ______ so early.',0,'{"answers": ["get up", "getting up", "got up", "have gotten up"], "success_answer": "getting up"}',NULL,2),
	 ('______ bag is this? — Its Marias.',0,'{"answers": ["Who", "Whom", "Whose", "Which"], "success_answer": "Whose"}',19,2),
	 ('I enjoy ______ in the park.',0,'{"answers": ["to walk", "walk", "walking", "to walking"], "success_answer": "walking"}',19,2),
	 ('She said, "I am tired." -> She said that ______.',0,'{"answers": ["I am tired", "she is tired", "she was tired", "she were tired"], "success_answer": "she was tired"}',19,2),
	 ('Choose the word that is closest in meaning to "BIG":',0,'{"answers": ["small", "large", "tiny", "little"], "success_answer": "large"}',20,2),
	 ('The keys are ______ the table.',0,'{"answers": ["in", "on", "at", "by"], "success_answer": "on"}',20,2),
	 ('He told me he ______ a doctor.',0,'{"answers": ["is", "was", "were", "has been"], "success_answer": "was"}',20,2),
	 ('Its raining ______. Dont forget your umbrella.',0,'{"answers": ["cats and dogs", "fish and frogs", "buckets", "water and ice"], "success_answer": "cats and dogs"}',20,2),
	 ('Im not used to ______ so early.',0,'{"answers": ["get up", "getting up", "got up", "have gotten up"], "success_answer": "getting up"}',20,2),
	 ('Choose the word that is closest in meaning to "BIG":',0,'{"answers": ["small", "large", "tiny", "little"], "success_answer": "large"}',21,2),
	 ('The keys are ______ the table.',0,'{"answers": ["in", "on", "at", "by"], "success_answer": "on"}',21,2),
	 ('He told me he ______ a doctor.',0,'{"answers": ["is", "was", "were", "has been"], "success_answer": "was"}',21,2),
	 ('Its raining ______. Dont forget your umbrella.',0,'{"answers": ["cats and dogs", "fish and frogs", "buckets", "water and ice"], "success_answer": "cats and dogs"}',21,2),
	 ('Im not used to ______ so early.',0,'{"answers": ["get up", "getting up", "got up", "have gotten up"], "success_answer": "getting up"}',21,2),
	 ('Choose the word that is closest in meaning to "BIG":',0,'{"answers": ["small", "large", "tiny", "little"], "success_answer": "large"}',30,2),
	 ('The keys are ______ the table.',0,'{"answers": ["in", "on", "at", "by"], "success_answer": "on"}',30,2),
	 ('He told me he ______ a doctor.',0,'{"answers": ["is", "was", "were", "has been"], "success_answer": "was"}',30,2),
	 ('Its raining ______. Dont forget your umbrella.',0,'{"answers": ["cats and dogs", "fish and frogs", "buckets", "water and ice"], "success_answer": "cats and dogs"}',30,2),
	 ('Im not used to ______ so early.',0,'{"answers": ["get up", "getting up", "got up", "have gotten up"], "success_answer": "getting up"}',30,2),
	 ('Choose the word that is closest in meaning to "BIG":',0,'{"answers": ["small", "large", "tiny", "little"], "success_answer": "large"}',31,2),
	 ('The keys are ______ the table.',0,'{"answers": ["in", "on", "at", "by"], "success_answer": "on"}',31,2),
	 ('He told me he ______ a doctor.',0,'{"answers": ["is", "was", "were", "has been"], "success_answer": "was"}',31,2),
	 ('Its raining ______. Dont forget your umbrella.',0,'{"answers": ["cats and dogs", "fish and frogs", "buckets", "water and ice"], "success_answer": "cats and dogs"}',31,2),
	 ('Im not used to ______ so early.',0,'{"answers": ["get up", "getting up", "got up", "have gotten up"], "success_answer": "getting up"}',31,2),
	 ('Choose the word that is closest in meaning to "BIG":',0,'{"answers": ["small", "large", "tiny", "little"], "success_answer": "large"}',32,2),
	 ('The keys are ______ the table.',0,'{"answers": ["in", "on", "at", "by"], "success_answer": "on"}',32,2),
	 ('He told me he ______ a doctor.',0,'{"answers": ["is", "was", "were", "has been"], "success_answer": "was"}',32,2),
	 ('Its raining ______. Dont forget your umbrella.',0,'{"answers": ["cats and dogs", "fish and frogs", "buckets", "water and ice"], "success_answer": "cats and dogs"}',32,2),
	 ('Im not used to ______ so early.',0,'{"answers": ["get up", "getting up", "got up", "have gotten up"], "success_answer": "getting up"}',32,2),
	 ('Choose the word that is closest in meaning to "BIG":',0,'{"answers": ["small", "large", "tiny", "little"], "success_answer": "large"}',33,2),
	 ('The keys are ______ the table.',0,'{"answers": ["in", "on", "at", "by"], "success_answer": "on"}',33,2),
	 ('He told me he ______ a doctor.',0,'{"answers": ["is", "was", "were", "has been"], "success_answer": "was"}',33,2),
	 ('Its raining ______. Dont forget your umbrella.',0,'{"answers": ["cats and dogs", "fish and frogs", "buckets", "water and ice"], "success_answer": "cats and dogs"}',33,2),
	 ('Im not used to ______ so early.',0,'{"answers": ["get up", "getting up", "got up", "have gotten up"], "success_answer": "getting up"}',33,2),
	 ('Choose the word that is closest in meaning to "BIG":',0,'{"answers": ["small", "large", "tiny", "little"], "success_answer": "large"}',44,2),
	 ('The keys are ______ the table.',0,'{"answers": ["in", "on", "at", "by"], "success_answer": "on"}',44,2),
	 ('He told me he ______ a doctor.',0,'{"answers": ["is", "was", "were", "has been"], "success_answer": "was"}',44,2),
	 ('Its raining ______. Dont forget your umbrella.',0,'{"answers": ["cats and dogs", "fish and frogs", "buckets", "water and ice"], "success_answer": "cats and dogs"}',44,2),
	 ('Im not used to ______ so early.',0,'{"answers": ["get up", "getting up", "got up", "have gotten up"], "success_answer": "getting up"}',44,2);


/*
	Заполнение связей
*/
INSERT INTO public.answers (user_id,exercise_id,answer) VALUES
	 (1,29,'some breads'),
	 (1,30,'is living'),
	 (1,31,'is built'),
	 (1,22,'a'),
	 (1,27,'will rain'),
	 (1,28,'turn off'),
	 (1,20,'am going'),
	 (1,23,'at'),
	 (1,24,'most exciting'),
	 (1,21,'can'),
	 (1,25,'you'),
	 (1,26,'are you doing'),
	 (1,50,'tiny'),
	 (1,51,'on'),
	 (1,52,'were'),
	 (1,53,'water and ice'),
	 (1,54,'get up'),
	 (1,11,'am'),
	 (1,4,'Are'),
	 (1,5,'am');

INSERT INTO public.courses_modules (course_id,module_id) VALUES
	 (4,1),
	 (6,1),
	 (1,2),
	 (4,2),
	 (6,2),
	 (1,4),
	 (1,7),
	 (1,8),
	 (1,9),
	 (1,10),
	 (1,11),
	 (1,12),
	 (1,13),
	 (1,1),
	 (1,14);

INSERT INTO public.courses_users (course_id,user_id) VALUES
	 (5,1);