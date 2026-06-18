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
                .nombre("Mentoria para Emprendedores")
                .tipo("MENTORIA")
                .descripcion("Programa de acompanamiento de emprendedores locales por parte de empresarios exitosos")
                .municipio("Florianopolis").cluster("CENTRO_HISTORICO")
                .organizacion("Associacao Comercial de Florianopolis").liderReferente("Carlos Silva")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://acfloripa.org.br/mentoria")
                .fechaInicio(LocalDate.of(2024,2,1)).fechaFin(null).activo(true).build(),

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
                .nombre("Curso de Programacion en Python")
                .tipo("FORMACION")
                .descripcion("Introduccion a Python y analisis de datos")
                .municipio("Florianopolis").cluster("UFSC")
                .organizacion("Universidad Federal de Santa Catarina").liderReferente(null)
                .replicable(0).impactoEstimado("ALTO")
                .urlReferencia("https://ufsc.br/cursos/python")
                .fechaInicio(LocalDate.of(2024,1,10)).fechaFin(LocalDate.of(2024,7,15)).activo(true).build(),

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
                .nombre("Experiencia de Voluntariado en Salud")
                .tipo("EXPERIENCIA")
                .descripcion("Voluntariado en hospitales locales para jovenes")
                .municipio("Sao Jose").cluster("SAO_JOSE_KOBRASOL")
                .organizacion("Cruz Roja Brasileña").liderReferente("Pedro Mendes")
                .replicable(0).impactoEstimado("ALTO")
                .urlReferencia("https://cruzroja.org.br/voluntariado-salud")
                .fechaInicio(LocalDate.of(2024,4,1)).fechaFin(LocalDate.of(2024,11,30)).activo(true).build(),

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
                .nombre("Mentoria para Artistas")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento a artistas locales en la gestion de sus carreras")
                .municipio("Florianopolis").cluster("CAMPECHE")
                .organizacion("Centro Cultural de Florianopolis").liderReferente("Lucia Almeida")
                .replicable(1).impactoEstimado("BAJO")
                .urlReferencia("https://ccfloripa.org.br/mentoria-artistas")
                .fechaInicio(LocalDate.of(2024,2,20)).fechaFin(null).activo(false).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Educacion Ambiental")
                .tipo("EXPERIENCIA")
                .descripcion("Talleres de educacion ambiental en escuelas")
                .municipio("Sao Jose").cluster("SAO_JOSE_ROCADO")
                .organizacion("ONG EcoAcao").liderReferente("Joao Fernandes")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://ecoacao.org.br/educacion-ambiental")
                .fechaInicio(LocalDate.of(2024,5,1)).fechaFin(LocalDate.of(2024,12,15)).activo(true).build(),

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
                .nombre("Mentoria en Gestion de Proyectos")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento en metodologias agiles y gestion de proyectos")
                .municipio("Florianopolis").cluster("JURERE")
                .organizacion("PMI Santa Catarina").liderReferente("Ricardo Gomes")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://pmisc.org.br/mentoria-proyectos")
                .fechaInicio(LocalDate.of(2024,3,10)).fechaFin(null).activo(true).build(),

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
                .nombre("Programa de Formacion en Ingles")
                .tipo("FORMACION")
                .descripcion("Curso de ingles para profesionales")
                .municipio("Florianopolis").cluster("RESIDENCIAL_NORTE")
                .organizacion("Language Center").liderReferente(null)
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://languagecenter.com.br/ingles")
                .fechaInicio(LocalDate.of(2024,2,1)).fechaFin(LocalDate.of(2024,9,30)).activo(true).build(),

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
                .nombre("Experiencia en Mantenimiento de Espacios Publicos")
                .tipo("EXPERIENCIA")
                .descripcion("Voluntariado en mantenimiento de parques y plazas")
                .municipio("Sao Jose").cluster("PALHOCA_PEDRA_BRANCA")
                .organizacion("Prefeitura de Sao Jose").liderReferente("Marcos Silva")
                .replicable(0).impactoEstimado("MEDIO")
                .urlReferencia("https://saojose.sc.gov.br/voluntariado")
                .fechaInicio(LocalDate.of(2024,5,15)).fechaFin(LocalDate.of(2024,12,31)).activo(true).build(),

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
                .nombre("Mentoria para Jovenes Profesionales")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento en insercion laboral y desarrollo profesional")
                .municipio("Florianopolis").cluster("VIA_EXPRESSA_CORREDOR")
                .organizacion("Fundacion Jovenes Profesionales").liderReferente("Fernanda Lima")
                .replicable(1).impactoEstimado("ALTO")
                .urlReferencia("https://fjp.org.br/mentoria-jovenes")
                .fechaInicio(LocalDate.of(2024,5,1)).fechaFin(null).activo(true).build(),

            SocialProgram.builder()
                .nombre("Experiencia en Educacion Infantil")
                .tipo("EXPERIENCIA")
                .descripcion("Ayuda en guarderias y educacion temprana")
                .municipio("Sao Jose").cluster("PALHOCA_CENTRO")
                .organizacion("ONG Educacion para Todos").liderReferente("Juliana Castro")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://educacionparatodos.org.br/infantil")
                .fechaInicio(LocalDate.of(2024,7,1)).fechaFin(LocalDate.of(2024,12,31)).activo(true).build(),

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
                .nombre("Mentoria en Contenido Digital")
                .tipo("MENTORIA")
                .descripcion("Acompañamiento en creacion de contenido para redes sociales")
                .municipio("Florianopolis").cluster("CBD_BEIRAMAR")
                .organizacion("Agencia de Contenidos Creativos").liderReferente("Gustavo Santos")
                .replicable(1).impactoEstimado("MEDIO")
                .urlReferencia("https://accreativos.com.br/mentoria-contenido")
                .fechaInicio(LocalDate.of(2024,6,15)).fechaFin(null).activo(true).build()
        ));
    }
}