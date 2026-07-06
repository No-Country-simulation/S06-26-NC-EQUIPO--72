package com.example.appbitb2g.seed;

import com.example.appbitb2g.model.SocialProgram;
import com.example.appbitb2g.repository.SocialProgramRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.List;

@Component
@Profile("dev")
public class SocialProgramSeeder {

    @Autowired private SocialProgramRepository repo;

    public void seed() {
        if (repo.count() > 0) return;

        repo.saveAll(List.of(

            //  Florianópolis 

            SocialProgram.builder()
                .nombre("Programa de Formacion en Tecnologias Web")
                .tipo("FORMACION")
                .descripcion("Curso intensivo de HTML, CSS y JavaScript para jovenes de 18 a 25 anos")
                .municipio("Florianopolis").cluster("TRINDADE")
                .organizacion("Prefeitura de Florianopolis").liderReferente(null)
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://floripa.gov.br/formacion-web")
                .fechaInicio(LocalDate.of(2024,1,15)).fechaFin(LocalDate.of(2024,6,30)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Arte Urbano Comunitario")
                .tipo("EXPERIENCIA")
                .descripcion("Intervencion artistica en espacios publicos junto a artistas locales")
                .municipio("Florianopolis").cluster("TRINDADE")
                .organizacion("Coletivo Arte Viva Floripa").liderReferente("Bruno Tavares")
                .replicable(1).impactoEstimado("BAJO")
                .urlReferencia("https://arteviva.org.br/arte-urbano")
                .fechaInicio(LocalDate.of(2024,4,1)).fechaFin(LocalDate.of(2024,10,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria para Emprendedores")
                .tipo("MENTORIA")
                .descripcion("Programa de acompanamiento de emprendedores locales por parte de empresarios exitosos")
                .municipio("Florianopolis").cluster("CENTRO_HISTORICO")
                .organizacion("Associacao Comercial de Florianopolis").liderReferente("Carlos Silva")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://acfloripa.org.br/mentoria")
                .fechaInicio(LocalDate.of(2024,2,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia de Voluntariado en Bibliotecas")
                .tipo("EXPERIENCIA")
                .descripcion("Apoyo a lectores y organizacion de fondos bibliograficos en bibliotecas comunitarias")
                .municipio("Florianopolis").cluster("CENTRO_HISTORICO")
                .organizacion("Rede de Bibliotecas de Florianopolis").liderReferente("Sandra Oliveira")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://bibliotecas.floripa.gov.br/voluntariado")
                .fechaInicio(LocalDate.of(2024,3,1)).fechaFin(LocalDate.of(2024,12,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Curso de Programacion en Python")
                .tipo("FORMACION")
                .descripcion("Introduccion a Python y analisis de datos")
                .municipio("Florianopolis").cluster("UFSC")
                .organizacion("Universidad Federal de Santa Catarina").liderReferente(null)
                .replicable(0).impactoEstimado("ALTO")
                .urlReferencia("https://ufsc.br/cursos/python")
                .fechaInicio(LocalDate.of(2024,1,10)).fechaFin(LocalDate.of(2024,7,15)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Apoyo a Adultos Mayores")
                .tipo("EXPERIENCIA")
                .descripcion("Visitas y actividades recreativas en hogares de ancianos de la region")
                .municipio("Florianopolis").cluster("UFSC")
                .organizacion("Instituto Cuidar Florianopolis").liderReferente("Beatriz Campos")
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://institutocuidar.org.br/adultos-mayores")
                .fechaInicio(LocalDate.of(2024,5,1)).fechaFin(LocalDate.of(2024,12,15)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Desarrollo Personal")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento en habilidades blandas y crecimiento profesional")
                .municipio("Florianopolis").cluster("LAGOA_CONCEICAO")
                .organizacion("Instituto de Desarrollo Humano").liderReferente("Ana Costa")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://idh.org.br/mentoria-personal")
                .fechaInicio(LocalDate.of(2024,2,15)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Radio Comunitaria")
                .tipo("EXPERIENCIA")
                .descripcion("Produccion de contenido y conduccion de programas en radio comunitaria local")
                .municipio("Florianopolis").cluster("LAGOA_CONCEICAO")
                .organizacion("Radio Comunitaria Lagoa FM").liderReferente("Patricia Melo")
                .replicable(0).impactoEstimado("BAJO")
                .urlReferencia("https://lagoafm.com.br/voluntariado")
                .fechaInicio(LocalDate.of(2024,5,10)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Programa de Formacion en Marketing Digital")
                .tipo("FORMACION")
                .descripcion("Curso de redes sociales y marketing online")
                .municipio("Florianopolis").cluster("ESTREITO_CAPOEIRAS")
                .organizacion("Escuela de Negocios Digital").liderReferente(null)
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://endigital.com.br/marketing")
                .fechaInicio(LocalDate.of(2024,3,1)).fechaFin(LocalDate.of(2024,8,30)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Alfabetizacion Digital para Adultos")
                .tipo("EXPERIENCIA")
                .descripcion("Talleres practicos de uso del celular, internet y redes sociales para mayores de 50 anos")
                .municipio("Florianopolis").cluster("ESTREITO_CAPOEIRAS")
                .organizacion("ONG Inclusion Digital SC").liderReferente("Vanessa Borges")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://inclusaod.org.br/alfabetizacion")
                .fechaInicio(LocalDate.of(2024,7,1)).fechaFin(LocalDate.of(2024,12,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria para Artistas")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento a artistas locales en la gestion de sus carreras")
                .municipio("Florianopolis").cluster("CAMPECHE")
                .organizacion("Centro Cultural de Florianopolis").liderReferente("Lucia Almeida")
                .replicable(1).impactoEstimado("BAJO")
                .urlReferencia("https://ccfloripa.org.br/mentoria-artistas")
                .fechaInicio(LocalDate.of(2024,2,20)).fechaFin(null).activo(false).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Monitoreo Ambiental Costero")
                .tipo("EXPERIENCIA")
                .descripcion("Recoleccion de datos y limpieza de playas con equipos de investigacion")
                .municipio("Florianopolis").cluster("CAMPECHE")
                .organizacion("Instituto Oceanografico Sul").liderReferente("Rafael Duarte")
                .replicable(0).impactoEstimado("ALTO")
                .urlReferencia("https://ios.org.br/monitoreo-costero")
                .fechaInicio(LocalDate.of(2024,6,1)).fechaFin(LocalDate.of(2024,11,30)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Curso de Diseno UX/UI")
                .tipo("FORMACION")
                .descripcion("Formacion en diseno de experiencia de usuario")
                .municipio("Florianopolis").cluster("COQUEIROS")
                .organizacion("Instituto de Diseno").liderReferente(null)
                .replicable(0).impactoEstimado("ALTO")
                .urlReferencia("https://institutodediseno.com.br/ux-ui")
                .fechaInicio(LocalDate.of(2024,4,15)).fechaFin(LocalDate.of(2024,10,30)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Deporte Adaptado")
                .tipo("EXPERIENCIA")
                .descripcion("Apoyo en actividades deportivas para personas con discapacidad")
                .municipio("Florianopolis").cluster("COQUEIROS")
                .organizacion("Asociacion Paralimpica de Santa Catarina").liderReferente("Diego Pimentel")
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://paralimpica-sc.org.br/voluntariado")
                .fechaInicio(LocalDate.of(2024,3,20)).fechaFin(LocalDate.of(2024,12,20)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Gestion de Proyectos")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento en metodologias agiles y gestion de proyectos")
                .municipio("Florianopolis").cluster("JURERE")
                .organizacion("PMI Santa Catarina").liderReferente("Ricardo Gomes")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://pmisc.org.br/mentoria-proyectos")
                .fechaInicio(LocalDate.of(2024,3,10)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Curso de Primeros Auxilios")
                .tipo("FORMACION")
                .descripcion("Capacitacion basica en primeros auxilios y RCP para la comunidad")
                .municipio("Florianopolis").cluster("JURERE")
                .organizacion("Cruz Roja Brasileña - Filial SC").liderReferente(null)
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://cruzroja.org.br/primeros-auxilios-floripa")
                .fechaInicio(LocalDate.of(2024,5,1)).fechaFin(LocalDate.of(2024,10,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Salvavidas Comunitario")
                .tipo("EXPERIENCIA")
                .descripcion("Formacion practica y apoyo a guardavidas en playas del norte de la isla")
                .municipio("Florianopolis").cluster("JURERE")
                .organizacion("Bombeiros Voluntarios Jurere").liderReferente("Alexandre Neves")
                .replicable(0).impactoEstimado("ALTO")
                .urlReferencia("https://bombeiros-jurere.org.br/voluntariado")
                .fechaInicio(LocalDate.of(2024,11,1)).fechaFin(LocalDate.of(2025,3,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Programa de Formacion en Ingles")
                .tipo("FORMACION")
                .descripcion("Curso de ingles para profesionales")
                .municipio("Florianopolis").cluster("RESIDENCIAL_NORTE")
                .organizacion("Language Center").liderReferente(null)
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://languagecenter.com.br/ingles")
                .fechaInicio(LocalDate.of(2024,2,1)).fechaFin(LocalDate.of(2024,9,30)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Economia del Hogar")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento en planificacion familiar y ahorro energetico para familias")
                .municipio("Florianopolis").cluster("RESIDENCIAL_NORTE")
                .organizacion("Instituto Familia Sustentable").liderReferente("Rosana Teixeira")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://ifamiliasustentavel.org.br/mentoria")
                .fechaInicio(LocalDate.of(2024,6,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Patrulla Escolar Comunitaria")
                .tipo("EXPERIENCIA")
                .descripcion("Apoyo en la seguridad vial y acompañamiento de estudiantes en cruces escolares")
                .municipio("Florianopolis").cluster("RESIDENCIAL_NORTE")
                .organizacion("DETRAN-SC - Educacion Vial").liderReferente("Hugo Cardoso")
                .replicable(1).impactoEstimado("BAJO")
                .urlReferencia("https://detran.sc.gov.br/patrulla-escolar")
                .fechaInicio(LocalDate.of(2024,3,1)).fechaFin(LocalDate.of(2024,12,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Finanzas Personales")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento en gestion de finanzas personales")
                .municipio("Florianopolis").cluster("SC401_CORREDOR")
                .organizacion("Instituto de Finanzas Personales").liderReferente("Paula Ribeiro")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://ifp.org.br/mentoria-finanzas")
                .fechaInicio(LocalDate.of(2024,4,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Curso de Seguridad Vial para Motociclistas")
                .tipo("FORMACION")
                .descripcion("Capacitacion en conduccion segura y normativa de transito para motos")
                .municipio("Florianopolis").cluster("SC401_CORREDOR")
                .organizacion("DETRAN-SC - Nucleo Florianopolis").liderReferente(null)
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://detran.sc.gov.br/curso-motociclistas")
                .fechaInicio(LocalDate.of(2024,4,1)).fechaFin(LocalDate.of(2024,10,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Gestion de Residuos Electronicos")
                .tipo("EXPERIENCIA")
                .descripcion("Recoleccion y clasificacion de residuos electronicos en puntos de la comunidad")
                .municipio("Florianopolis").cluster("SC401_CORREDOR")
                .organizacion("EcoTech Floripa").liderReferente("Adriana Costa")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://ecotech.floripa.br/residuos-electronicos")
                .fechaInicio(LocalDate.of(2024,5,20)).fechaFin(LocalDate.of(2024,11,20)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Curso de Fotografia Digital")
                .tipo("FORMACION")
                .descripcion("Aprendizaje de fotografia y edicion de imagenes")
                .municipio("Florianopolis").cluster("INGLESES")
                .organizacion("Escuela de Arte Visual").liderReferente(null)
                .replicable(1).impactoEstimado("BAJO")
                .urlReferencia("https://eav.com.br/fotografia")
                .fechaInicio(LocalDate.of(2024,3,15)).fechaFin(LocalDate.of(2024,8,15)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Turismo Sustentable")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento a emprendedores turisticos en practicas sustentables")
                .municipio("Florianopolis").cluster("INGLESES")
                .organizacion("Santur - Turismo Sustentable SC").liderReferente("Eliane Borba")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://santur.sc.gov.br/mentoria-turismo")
                .fechaInicio(LocalDate.of(2024,4,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Huerta Escolar")
                .tipo("EXPERIENCIA")
                .descripcion("Implementacion y mantenimiento de huertas en escuelas publicas")
                .municipio("Florianopolis").cluster("INGLESES")
                .organizacion("Red de Escuelas Sostenibles Floripa").liderReferente("Tatiana Moraes")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://redesostenible.floripa.br/huerta")
                .fechaInicio(LocalDate.of(2024,4,15)).fechaFin(LocalDate.of(2024,11,15)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria para Jovenes Profesionales")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento en insercion laboral y desarrollo profesional")
                .municipio("Florianopolis").cluster("VIA_EXPRESSA_CORREDOR")
                .organizacion("Fundacion Jovenes Profesionales").liderReferente("Fernanda Lima")
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://fjp.org.br/mentoria-jovenes")
                .fechaInicio(LocalDate.of(2024,5,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Curso de Atencion al Cliente y Ventas")
                .tipo("FORMACION")
                .descripcion("Tecnicas de ventas, comunicacion y servicio al cliente para comerciantes")
                .municipio("Florianopolis").cluster("VIA_EXPRESSA_CORREDOR")
                .organizacion("CDL Florianopolis").liderReferente(null)
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://cdlflorianopolis.org.br/curso-ventas")
                .fechaInicio(LocalDate.of(2024,6,10)).fechaFin(LocalDate.of(2024,11,10)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Feria de Empleo")
                .tipo("EXPERIENCIA")
                .descripcion("Organizacion y apoyo a ferias de inclusion laboral para jovenes desempleados")
                .municipio("Florianopolis").cluster("VIA_EXPRESSA_CORREDOR")
                .organizacion("SINE Florianopolis").liderReferente("Camila Rodrigues")
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://sine.sc.gov.br/feria-empleo")
                .fechaInicio(LocalDate.of(2024,8,15)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Programa de Formacion en IoT")
                .tipo("FORMACION")
                .descripcion("Curso de Internet de las Cosas y automatizacion")
                .municipio("Florianopolis").cluster("AEROPORTO_HLZ")
                .organizacion("Instituto de Tecnologia Avanzada").liderReferente(null)
                .replicable(0).impactoEstimado("ALTO")
                .urlReferencia("https://ita.com.br/iot")
                .fechaInicio(LocalDate.of(2024,6,1)).fechaFin(LocalDate.of(2024,11,30)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Logistica y Cadena de Suministro")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento a profesionales del sector logistico y de transporte")
                .municipio("Florianopolis").cluster("AEROPORTO_HLZ")
                .organizacion("ABOL - Asociacion Brasileña de Operadores Logisticos SC").liderReferente("Sergio Nunes")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://abol-sc.org.br/mentoria")
                .fechaInicio(LocalDate.of(2024,7,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Atencion al Viajero")
                .tipo("EXPERIENCIA")
                .descripcion("Voluntariado en informacion turistica para pasajeros en el aeropuerto y terminal de buses")
                .municipio("Florianopolis").cluster("AEROPORTO_HLZ")
                .organizacion("Santur - Turismo de Santa Catarina").liderReferente("Renata Barros")
                .replicable(0).impactoEstimado("BAJO")
                .urlReferencia("https://santur.sc.gov.br/voluntariado-aeropuerto")
                .fechaInicio(LocalDate.of(2024,10,1)).fechaFin(LocalDate.of(2025,2,28)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Contenido Digital")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento en creacion de contenido para redes sociales")
                .municipio("Florianopolis").cluster("CBD_BEIRAMAR")
                .organizacion("Agencia de Contenidos Creativos").liderReferente("Gustavo Santos")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://accreativos.com.br/mentoria-contenido")
                .fechaInicio(LocalDate.of(2024,6,15)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Curso de Gestion Cultural")
                .tipo("FORMACION")
                .descripcion("Administracion de proyectos y espacios culturales para gestores emergentes")
                .municipio("Florianopolis").cluster("CBD_BEIRAMAR")
                .organizacion("Fundacion Cultural de Florianopolis Franklin Cascaes").liderReferente(null)
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://fundacultural.floripa.gov.br/gestion-cultural")
                .fechaInicio(LocalDate.of(2024,8,1)).fechaFin(LocalDate.of(2024,12,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Feria de Economia Solidaria")
                .tipo("EXPERIENCIA")
                .descripcion("Organizacion y atencion en ferias de productos artesanales y de economia solidaria")
                .municipio("Florianopolis").cluster("CBD_BEIRAMAR")
                .organizacion("Red de Economia Solidaria SC").liderReferente("Claudia Ferreira")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://ecosolidaria-sc.org.br/feria")
                .fechaInicio(LocalDate.of(2024,9,1)).fechaFin(null).activo(true).build(),

            //  Sao Jose 

            SocialProgram.builder()
                .nombre("Experiencia Comunitaria en Jardinagem")
                .tipo("EXPERIENCIA")
                .descripcion("Proyecto de cuidado de espacios publicos con participacion de la comunidad")
                .municipio("Sao Jose").cluster("SAO_JOSE_CENTRO")
                .organizacion("ONG Verde Vida").liderReferente("Maria Souza")
                .replicable(1).impactoEstimado("BAJO")
                .urlReferencia("https://verde-vida.org/jardines")
                .fechaInicio(LocalDate.of(2024,3,1)).fechaFin(LocalDate.of(2024,12,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Curso de Emprendimiento Social")
                .tipo("FORMACION")
                .descripcion("Capacitacion en modelos de negocio con impacto social para jovenes")
                .municipio("Sao Jose").cluster("SAO_JOSE_CENTRO")
                .organizacion("Sebrae Sao Jose").liderReferente(null)
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://sebrae.com.br/saojose/emprendimiento-social")
                .fechaInicio(LocalDate.of(2024,4,1)).fechaFin(LocalDate.of(2024,10,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Comunicacion Comunitaria")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento a lideres vecinales en comunicacion efectiva y gestion de conflictos")
                .municipio("Sao Jose").cluster("SAO_JOSE_CENTRO")
                .organizacion("Instituto Liderazgo Comunitario SC").liderReferente("Flavia Andrade")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://ilcsc.org.br/mentoria-comunicacion")
                .fechaInicio(LocalDate.of(2024,5,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia de Voluntariado en Salud")
                .tipo("EXPERIENCIA")
                .descripcion("Voluntariado en hospitales locales para jovenes")
                .municipio("Sao Jose").cluster("SAO_JOSE_KOBRASOL")
                .organizacion("Cruz Roja Brasileña").liderReferente("Pedro Mendes")
                .replicable(0).impactoEstimado("ALTO")
                .urlReferencia("https://cruzroja.org.br/voluntariado-salud")
                .fechaInicio(LocalDate.of(2024,4,1)).fechaFin(LocalDate.of(2024,11,30)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Curso de Auxiliar de Farmacia")
                .tipo("FORMACION")
                .descripcion("Formacion tecnica en atencion farmaceutica y manipulacion de medicamentos")
                .municipio("Sao Jose").cluster("SAO_JOSE_KOBRASOL")
                .organizacion("Escola Tecnica de Saude SC").liderReferente(null)
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://etss.com.br/auxiliar-farmacia")
                .fechaInicio(LocalDate.of(2024,3,1)).fechaFin(LocalDate.of(2024,9,30)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Salud Comunitaria")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento a agentes comunitarios de salud en prevencion y promocion")
                .municipio("Sao Jose").cluster("SAO_JOSE_KOBRASOL")
                .organizacion("Secretaria Municipal de Salud de Sao Jose").liderReferente("Mariana Fonseca")
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://saojose.sc.gov.br/mentoria-salud")
                .fechaInicio(LocalDate.of(2024,6,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Educacion Ambiental")
                .tipo("EXPERIENCIA")
                .descripcion("Talleres de educacion ambiental en escuelas")
                .municipio("Sao Jose").cluster("SAO_JOSE_ROÇADO")
                .organizacion("ONG EcoAcao").liderReferente("Joao Fernandes")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://ecoacao.org.br/educacion-ambiental")
                .fechaInicio(LocalDate.of(2024,5,1)).fechaFin(LocalDate.of(2024,12,15)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Curso de Construccion Sustentable")
                .tipo("FORMACION")
                .descripcion("Tecnicas de construccion con materiales reciclados y bajo impacto ambiental")
                .municipio("Sao Jose").cluster("SAO_JOSE_ROÇADO")
                .organizacion("Sinduscon Sao Jose").liderReferente(null)
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://sinduscon-sj.org.br/construccion-sustentable")
                .fechaInicio(LocalDate.of(2024,6,1)).fechaFin(LocalDate.of(2024,12,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Gestion de Residuos")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento a cooperativas de reciclaje en gestion y comercializacion")
                .municipio("Sao Jose").cluster("SAO_JOSE_ROÇADO")
                .organizacion("Catamare - Red de Catadores SC").liderReferente("Nilson Pereira")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://catamare-sc.org.br/mentoria")
                .fechaInicio(LocalDate.of(2024,7,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Cocina Comunitaria")
                .tipo("EXPERIENCIA")
                .descripcion("Talleres de cocina saludable y alimentacion comunitaria")
                .municipio("Sao Jose").cluster("SAO_JOSE_BARREIROS")
                .organizacion("ONG Comida Vida").liderReferente("Carla Nunes")
                .replicable(1).impactoEstimado("BAJO")
                .urlReferencia("https://comidavida.org.br/cocina")
                .fechaInicio(LocalDate.of(2024,6,1)).fechaFin(LocalDate.of(2024,12,20)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Curso de Gastronomia Popular")
                .tipo("FORMACION")
                .descripcion("Tecnicas culinarias y emprendimiento gastronomico para jovenes en situacion de vulnerabilidad")
                .municipio("Sao Jose").cluster("SAO_JOSE_BARREIROS")
                .organizacion("SENAC Sao Jose").liderReferente(null)
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://senac.br/saojose/gastronomia")
                .fechaInicio(LocalDate.of(2024,5,1)).fechaFin(LocalDate.of(2024,11,30)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Emprendimiento Local")
                .tipo("MENTORIA")
                .descripcion("Ayudar a pequeños empresarios a crecer")
                .municipio("Palhoca").cluster("SAO_JOSE_BARREIROS")
                .organizacion("Sebrae Palhoca").liderReferente("Ana Costa")
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://sebrae.com.br/palhoca/mentoria")
                .fechaInicio(LocalDate.of(2024,3,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Mantenimiento de Espacios Publicos")
                .tipo("EXPERIENCIA")
                .descripcion("Voluntariado en mantenimiento de parques y plazas")
                .municipio("Sao Jose").cluster("PALHOCA_PEDRA_BRANCA")
                .organizacion("Prefeitura de Sao Jose").liderReferente("Marcos Silva")
                .replicable(0).impactoEstimado("MEDIO")
                .urlReferencia("https://saojose.sc.gov.br/voluntariado")
                .fechaInicio(LocalDate.of(2024,5,15)).fechaFin(LocalDate.of(2024,12,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Educacion Infantil")
                .tipo("EXPERIENCIA")
                .descripcion("Ayuda en guarderias y educacion temprana")
                .municipio("Sao Jose").cluster("PALHOCA_CENTRO")
                .organizacion("ONG Educacion para Todos").liderReferente("Juliana Castro")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://educacionparatodos.org.br/infantil")
                .fechaInicio(LocalDate.of(2024,7,1)).fechaFin(LocalDate.of(2024,12,31)).activo(true).build(),

            //  Palhoca 

            SocialProgram.builder()
                .nombre("Curso de Agricultura Urbana")
                .tipo("FORMACION")
                .descripcion("Aprender a cultivar alimentos en espacios pequeños")
                .municipio("Palhoca").cluster("PALHOCA_CENTRO")
                .organizacion("Associacao de Agricultura Urbana de Palhoca").liderReferente("Marcia Silva")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://aupalhoca.org.br/curso-agricultura")
                .fechaInicio(LocalDate.of(2024,4,1)).fechaFin(LocalDate.of(2024,11,30)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Gestion de Microempresas")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento contable, fiscal y de gestion para microempresarios")
                .municipio("Palhoca").cluster("PALHOCA_CENTRO")
                .organizacion("Contaje - Consultoria Contable SC").liderReferente("Roberto Assuncao")
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://contaje.com.br/mentoria-microempresas")
                .fechaInicio(LocalDate.of(2024,5,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Reciclaje")
                .tipo("EXPERIENCIA")
                .descripcion("Voluntariado en puntos de reciclaje de la ciudad")
                .municipio("Palhoca").cluster("PALHOCA_PEDRA_BRANCA")
                .organizacion("Cooperativa de Reciclaje de Palhoca").liderReferente("Carlos Pereira")
                .replicable(0).impactoEstimado("BAJO")
                .urlReferencia("https://crpalhoca.org.br/voluntariado")
                .fechaInicio(LocalDate.of(2024,5,1)).fechaFin(LocalDate.of(2024,12,31)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Curso de Energia Solar Residencial")
                .tipo("FORMACION")
                .descripcion("Instalacion y mantenimiento de paneles solares para tecnicoss electricistas")
                .municipio("Palhoca").cluster("PALHOCA_PEDRA_BRANCA")
                .organizacion("SENAI Palhoca").liderReferente(null)
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://senai.br/palhoca/energia-solar")
                .fechaInicio(LocalDate.of(2024,6,1)).fechaFin(LocalDate.of(2024,12,15)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Transicion Energetica")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento a comercios y pymes en la adopcion de energias renovables")
                .municipio("Palhoca").cluster("PALHOCA_PEDRA_BRANCA")
                .organizacion("Instituto de Energia Renovable SC").liderReferente("Thiago Mello")
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://iers.org.br/mentoria-transicion")
                .fechaInicio(LocalDate.of(2024,7,1)).fechaFin(null).activo(true).build(),

            //  Biguacu 

            SocialProgram.builder()
                .nombre("Curso de Mantenimiento de Motocicletas")
                .tipo("FORMACION")
                .descripcion("Aprender a reparar y mantener motos")
                .municipio("Biguacu").cluster("BIGUACU_BR101_NORTE")
                .organizacion("Escuela Tecnica de Biguacu").liderReferente(null)
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://etbiguacu.com.br/curso-motos")
                .fechaInicio(LocalDate.of(2024,2,15)).fechaFin(LocalDate.of(2024,9,15)).activo(true).build(),

            SocialProgram.builder()
                .nombre("Mentoria en Comercio Rural")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento a productores rurales en comercializacion y acceso a mercados")
                .municipio("Biguacu").cluster("BIGUACU_BR101_NORTE")
                .organizacion("Epagri Biguacu").liderReferente("Valdir Schmitt")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://epagri.sc.gov.br/biguacu/mentoria-rural")
                .fechaInicio(LocalDate.of(2024,3,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Deporte Comunitario")
                .tipo("EXPERIENCIA")
                .descripcion("Organizar partidos de fútbol para niños y jóvenes")
                .municipio("Biguacu").cluster("BIGUACU_BR101_NORTE")
                .organizacion("Fundacion Deporte y Vida Biguacu").liderReferente("Roberto Lima")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://fdvbiguacu.org.br/futbol-comunitario")
                .fechaInicio(LocalDate.of(2024,4,15)).fechaFin(LocalDate.of(2024,12,15)).activo(true).build()
        ));
    }
}