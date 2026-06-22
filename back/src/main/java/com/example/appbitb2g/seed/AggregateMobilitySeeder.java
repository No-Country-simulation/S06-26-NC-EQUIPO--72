package com.example.appbitb2g.seed;

import com.example.appbitb2g.model.AggregateMobility;
import com.example.appbitb2g.repository.AggregateMobilityRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.List;

@Component
@Profile("dev")

public class AggregateMobilitySeeder {

    @Autowired
    private AggregateMobilityRepository aggregateMobilityRepository;

    public  void seed(){
        if (aggregateMobilityRepository.count() > 0)
            return;

        aggregateMobilityRepository.saveAll(List.of(
                new AggregateMobility(null, "724050684142457", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "MANHA", "C", "25-34", "WCDMA", 2, 49567151.0, 0.1163, 0.616),
                new AggregateMobility(null, "724050684142457", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "NOITE", "C", "25-34", "WCDMA", 5, 35678351.0, 0.1273, 0.496),
                new AggregateMobility(null, "724050684142457", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "TARDE", "C", "25-34", "WCDMA", 1, 18634729.0, 0.0731, 0.469),
                new AggregateMobility(null, "724050697605965", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "MADRUGADA", "C", "25-34", "WCDMA", 2, 34177344.0, 0.1539, 0.278),
                new AggregateMobility(null, "724050697605965", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "MANHA", "C", "25-34", "WCDMA", 6, 38344704.0, 0.1369, 0.311),
                new AggregateMobility(null, "724050697605965", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "NOITE", "C", "25-34", "WCDMA", 1, 14499831.0, 0.0746, 0.649),
                new AggregateMobility(null, "724050697342190", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "MADRUGADA", "C", "25-34", "WCDMA", 3, 21778196.0, 0.05, 0.687),
                new AggregateMobility(null, "724050697342190", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "TARDE", "C", "25-34", "WCDMA", 6, 46810360.0, 0.0777, 0.136),
                new AggregateMobility(null, "724050683983270", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "TARDE", "C", "25-34", "WCDMA", 1, 40465774.0, 0.1302, 0.06),
                new AggregateMobility(null, "724050683983270", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "TARDE", "C", "25-34", "WCDMA", 5, 15706915.0, 0.1501, 0.565),
                new AggregateMobility(null, "724050697342190", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-02"), "NOITE", "C", "25-34", "LTE", 6, 57997427.0, 0.0553, 0.309),
                new AggregateMobility(null, "7240501005162724", "CAMPECHE", "Florianopolis", LocalDate.parse("2026-03-02"), "NOITE", "C", "25-34", "LTE", 3, 19384220.0, 0.085, 0.575),
                new AggregateMobility(null, "7240501005162724", "CAMPECHE", "Florianopolis", LocalDate.parse("2026-03-02"), "NOITE", "C", "25-34", "LTE", 3, 30462967.0, 0.0911, 0.379),
                new AggregateMobility(null, "7240501005162724", "CAMPECHE", "Florianopolis", LocalDate.parse("2026-03-02"), "TARDE", "C", "25-34", "LTE", 4, 47584576.0, 0.1189, 0.451),
                new AggregateMobility(null, "7240501005162597", "LAGOA_CONCEICAO", "Florianopolis", LocalDate.parse("2026-03-02"), "NOITE", "C", "25-34", "LTE", 2, 50748493.0, 0.1054, 0.238),
                new AggregateMobility(null, "7240501005162597", "LAGOA_CONCEICAO", "Florianopolis", LocalDate.parse("2026-03-02"), "TARDE", "C", "25-34", "LTE", 2, 49658826.0, 0.0215, 0.048),
                new AggregateMobility(null, "7240501004550410", "UFSC", "Florianopolis", LocalDate.parse("2026-03-02"), "NOITE", "C", "25-34", "LTE", 2, 30870593.0, 0.116, 0.029),
                new AggregateMobility(null, "7240501004550410", "UFSC", "Florianopolis", LocalDate.parse("2026-03-02"), "NOITE", "C", "25-34", "LTE", 6, 60302140.0, 0.0886, 0.589),
                new AggregateMobility(null, "7240501005172207", "CAMPECHE", "Florianopolis", LocalDate.parse("2026-03-03"), "MANHA", "C", "25-34", "LTE", 3, 15019049.0, 0.0527, 0.396),
                new AggregateMobility(null, "7240501005172207", "CAMPECHE", "Florianopolis", LocalDate.parse("2026-03-03"), "NOITE", "C", "25-34", "LTE", 5, 13997748.0, 0.0102, 0.508)


                ));
    }

}
