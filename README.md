# DivineNexus_GodModeOverlordOfTheTechnoRealm
Divine Nexus: God Mode Overlord Of The Techno Realm

### Run RabbitMQ as channels layers backend
```
docker run -d --name rabbitmq_dn -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```
