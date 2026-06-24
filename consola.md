Appbitb2g_AI exited with code 1 (restarting)
Appbitb2g_AI          | INFO:     Will watch for changes in these directories: ['/app']
Appbitb2g_AI          | Traceback (most recent call last):
Appbitb2g_AI          |   File "/usr/local/bin/uvicorn", line 8, in <module>
Appbitb2g_AI          |     sys.exit(main())
Appbitb2g_AI          |              ^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1524, in __call__
Appbitb2g_AI          |     return self.main(*args, **kwargs)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1445, in main
Appbitb2g_AI          |     rv = self.invoke(ctx)
Appbitb2g_AI          |          ^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1308, in invoke
Appbitb2g_AI          |     return ctx.invoke(self.callback, **ctx.params)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 877, in invoke
Appbitb2g_AI          |     return callback(*args, **kwargs)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/main.py", line 441, in main
Appbitb2g_AI          |     run(
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/main.py", line 609, in run
Appbitb2g_AI          |     config.load_app()
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/config.py", line 415, in load_app
Appbitb2g_AI          |     return import_from_string(self.app)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/importer.py", line 19, in import_from_string
Appbitb2g_AI          |     module = importlib.import_module(module_str)
Appbitb2g_AI          |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
Appbitb2g_AI          |     return _bootstrap._gcd_import(name[level:], package, level)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
Appbitb2g_AI          |   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
Appbitb2g_AI          |   File "/app/main.py", line 3, in <module>
Appbitb2g_AI          |     from app.core.config import settings
Appbitb2g_AI          |   File "/app/app/core/config.py", line 18, in <module>
Appbitb2g_AI          |     settings = Settings()
Appbitb2g_AI          |                ^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/pydantic_settings/main.py", line 176, in __init__
Appbitb2g_AI          |     super().__init__(
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/pydantic/main.py", line 263, in __init__
Appbitb2g_AI          |     validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
Appbitb2g_AI          |                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          | pydantic_core._pydantic_core.ValidationError: 5 validation errors for Settings
Appbitb2g_AI          | db_host
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='db', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_port
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='3306', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_name
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='app_bit_b_2g_db', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_user
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='root', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_password
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='root', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI exited with code 1 (restarting)
Appbitb2g_AI          | INFO:     Will watch for changes in these directories: ['/app']
Appbitb2g_AI          | Traceback (most recent call last):
Appbitb2g_AI          |   File "/usr/local/bin/uvicorn", line 8, in <module>
Appbitb2g_AI          |     sys.exit(main())
Appbitb2g_AI          |              ^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1524, in __call__
Appbitb2g_AI          |     return self.main(*args, **kwargs)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1445, in main
Appbitb2g_AI          |     rv = self.invoke(ctx)
Appbitb2g_AI          |          ^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1308, in invoke
Appbitb2g_AI          |     return ctx.invoke(self.callback, **ctx.params)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 877, in invoke
Appbitb2g_AI          |     return callback(*args, **kwargs)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/main.py", line 441, in main
Appbitb2g_AI          |     run(
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/main.py", line 609, in run
Appbitb2g_AI          |     config.load_app()
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/config.py", line 415, in load_app
Appbitb2g_AI          |     return import_from_string(self.app)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/importer.py", line 19, in import_from_string
Appbitb2g_AI          |     module = importlib.import_module(module_str)
Appbitb2g_AI          |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
Appbitb2g_AI          |     return _bootstrap._gcd_import(name[level:], package, level)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
Appbitb2g_AI          |   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
Appbitb2g_AI          |   File "/app/main.py", line 3, in <module>
Appbitb2g_AI          |     from app.core.config import settings
Appbitb2g_AI          |   File "/app/app/core/config.py", line 18, in <module>
Appbitb2g_AI          |     settings = Settings()
Appbitb2g_AI          |                ^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/pydantic_settings/main.py", line 176, in __init__
Appbitb2g_AI          |     super().__init__(
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/pydantic/main.py", line 263, in __init__
Appbitb2g_AI          |     validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
Appbitb2g_AI          |                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          | pydantic_core._pydantic_core.ValidationError: 5 validation errors for Settings
Appbitb2g_AI          | db_host
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='db', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_port
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='3306', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_name
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='app_bit_b_2g_db', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_user
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='root', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_password
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='root', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI exited with code 1 (restarting)
Appbitb2g             | 2026-06-24T19:17:48.158Z  INFO 176 --- [appbitb2g] [nio-8080-exec-1] o.a.c.c.C.[Tomcat].[localhost].[/api]    : Initializing Spring DispatcherServlet 'dispatcherServlet'
Appbitb2g             | 2026-06-24T19:17:48.158Z  INFO 176 --- [appbitb2g] [nio-8080-exec-1] o.s.web.servlet.DispatcherServlet        : Initializing Servlet 'dispatcherServlet'
Appbitb2g             | 2026-06-24T19:17:48.160Z  INFO 176 --- [appbitb2g] [nio-8080-exec-1] o.s.web.servlet.DispatcherServlet        : Completed initialization in 2 ms
Appbitb2g             | 2026-06-24T19:17:49.395Z  INFO 176 --- [appbitb2g] [nio-8080-exec-5] o.springdoc.api.AbstractOpenApiResource  : Init duration for springdoc-openapi is: 745 ms
Appbitb2g_AI          | INFO:     Will watch for changes in these directories: ['/app']
Appbitb2g             | 2026-06-24T19:17:58.657Z ERROR 176 --- [appbitb2g] [nio-8080-exec-6] o.a.c.c.C.[.[.[.[dispatcherServlet]      : Servlet.service() for servlet [dispatcherServlet] in context with path [/api] threw exception [Request processing failed: org.springframework.web.client.ResourceAccessException: I/O error on POST request for "http://ai:8000/consulta": Connection refused] with root cause
Appbitb2g             | 
Appbitb2g             | java.net.ConnectException: Connection refused
Appbitb2g             |         at java.base/sun.nio.ch.Net.connect0(Native Method) ~[na:na]
Appbitb2g             |         at java.base/sun.nio.ch.Net.connect(Net.java:601) ~[na:na]
Appbitb2g             |         at java.base/sun.nio.ch.Net.connect(Net.java:590) ~[na:na]
Appbitb2g             |         at java.base/sun.nio.ch.NioSocketImpl.connect(NioSocketImpl.java:583) ~[na:na]
Appbitb2g             |         at java.base/java.net.Socket.connect(Socket.java:751) ~[na:na]
Appbitb2g             |         at java.base/java.net.Socket.connect(Socket.java:686) ~[na:na]
Appbitb2g             |         at java.base/sun.net.NetworkClient.doConnect(NetworkClient.java:183) ~[na:na]
Appbitb2g             |         at java.base/sun.net.www.http.HttpClient.openServer(HttpClient.java:531) ~[na:na]
Appbitb2g             |         at java.base/sun.net.www.http.HttpClient.openServer(HttpClient.java:636) ~[na:na]
Appbitb2g             |         at java.base/sun.net.www.http.HttpClient.<init>(HttpClient.java:282) ~[na:na]
Appbitb2g             |         at java.base/sun.net.www.http.HttpClient.New(HttpClient.java:386) ~[na:na]
Appbitb2g             |         at java.base/sun.net.www.http.HttpClient.New(HttpClient.java:408) ~[na:na]
Appbitb2g             |         at java.base/sun.net.www.protocol.http.HttpURLConnection.getNewHttpClient(HttpURLConnection.java:1324) ~[na:na]
Appbitb2g             |         at java.base/sun.net.www.protocol.http.HttpURLConnection.plainConnect0(HttpURLConnection.java:1257) ~[na:na]
Appbitb2g             |         at java.base/sun.net.www.protocol.http.HttpURLConnection.plainConnect(HttpURLConnection.java:1143) ~[na:na]
Appbitb2g             |         at java.base/sun.net.www.protocol.http.HttpURLConnection.connect(HttpURLConnection.java:1072) ~[na:na]
Appbitb2g             |         at org.springframework.http.client.SimpleClientHttpRequest.executeInternal(SimpleClientHttpRequest.java:80) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.http.client.AbstractStreamingClientHttpRequest.executeInternal(AbstractStreamingClientHttpRequest.java:87) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.http.client.AbstractClientHttpRequest.execute(AbstractClientHttpRequest.java:80) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.client.RestTemplate.doExecute(RestTemplate.java:754) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.client.RestTemplate.execute(RestTemplate.java:677) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.client.RestTemplate.postForObject(RestTemplate.java:401) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at com.example.appbitb2g.service.impl.DataServiceImp.aiQueryAgent(DataServiceImp.java:37) ~[classes/:na]
Appbitb2g             |         at com.example.appbitb2g.controller.DataController.datosQuery(DataController.java:54) ~[classes/:na]
Appbitb2g             |         at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:103) ~[na:na]
Appbitb2g             |         at java.base/java.lang.reflect.Method.invoke(Method.java:580) ~[na:na]
Appbitb2g             |         at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:252) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:184) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:117) ~[spring-webmvc-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:934) ~[spring-webmvc-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:853) ~[spring-webmvc-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:86) ~[spring-webmvc-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:963) ~[spring-webmvc-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:866) ~[spring-webmvc-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1000) ~[spring-webmvc-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:903) ~[spring-webmvc-7.0.7.jar:7.0.7]
Appbitb2g             |         at jakarta.servlet.http.HttpServlet.service(HttpServlet.java:649) ~[tomcat-embed-core-11.0.21.jar:6.1]
Appbitb2g             |         at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:874) ~[spring-webmvc-7.0.7.jar:7.0.7]
Appbitb2g             |         at jakarta.servlet.http.HttpServlet.service(HttpServlet.java:710) ~[tomcat-embed-core-11.0.21.jar:6.1]
Appbitb2g             |         at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:128) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:53) ~[tomcat-embed-websocket-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:107) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.springframework.web.filter.RequestContextFilter.doFilterInternal(RequestContextFilter.java:100) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:107) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.springframework.web.filter.FormContentFilter.doFilterInternal(FormContentFilter.java:93) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:107) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:199) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116) ~[spring-web-7.0.7.jar:7.0.7]
Appbitb2g             |         at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:107) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:165) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:77) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:492) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:113) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:83) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:72) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:341) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:397) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:63) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:903) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1801) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:52) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.tomcat.util.threads.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:946) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.tomcat.util.threads.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:480) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:57) ~[tomcat-embed-core-11.0.21.jar:11.0.21]
Appbitb2g             |         at java.base/java.lang.Thread.run(Thread.java:1583) ~[na:na]
Appbitb2g             | 
Appbitb2g_AI          | Traceback (most recent call last):
Appbitb2g_AI          |   File "/usr/local/bin/uvicorn", line 8, in <module>
Appbitb2g_AI          |     sys.exit(main())
Appbitb2g_AI          |              ^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1524, in __call__
Appbitb2g_AI          |     return self.main(*args, **kwargs)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1445, in main
Appbitb2g_AI          |     rv = self.invoke(ctx)
Appbitb2g_AI          |          ^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1308, in invoke
Appbitb2g_AI          |     return ctx.invoke(self.callback, **ctx.params)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 877, in invoke
Appbitb2g_AI          |     return callback(*args, **kwargs)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/main.py", line 441, in main
Appbitb2g_AI          |     run(
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/main.py", line 609, in run
Appbitb2g_AI          |     config.load_app()
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/config.py", line 415, in load_app
Appbitb2g_AI          |     return import_from_string(self.app)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/importer.py", line 19, in import_from_string
Appbitb2g_AI          |     module = importlib.import_module(module_str)
Appbitb2g_AI          |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
Appbitb2g_AI          |     return _bootstrap._gcd_import(name[level:], package, level)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
Appbitb2g_AI          |   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
Appbitb2g_AI          |   File "/app/main.py", line 3, in <module>
Appbitb2g_AI          |     from app.core.config import settings
Appbitb2g_AI          |   File "/app/app/core/config.py", line 18, in <module>
Appbitb2g_AI          |     settings = Settings()
Appbitb2g_AI          |                ^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/pydantic_settings/main.py", line 176, in __init__
Appbitb2g_AI          |     super().__init__(
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/pydantic/main.py", line 263, in __init__
Appbitb2g_AI          |     validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
Appbitb2g_AI          |                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          | pydantic_core._pydantic_core.ValidationError: 5 validation errors for Settings
Appbitb2g_AI          | db_host
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='db', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_port
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='3306', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_name
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='app_bit_b_2g_db', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_user
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='root', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_password
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='root', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI exited with code 1 (restarting)
Appbitb2g_AI          | INFO:     Will watch for changes in these directories: ['/app']
Appbitb2g_AI          | Traceback (most recent call last):
Appbitb2g_AI          |   File "/usr/local/bin/uvicorn", line 8, in <module>
Appbitb2g_AI          |     sys.exit(main())
Appbitb2g_AI          |              ^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1524, in __call__
Appbitb2g_AI          |     return self.main(*args, **kwargs)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1445, in main
Appbitb2g_AI          |     rv = self.invoke(ctx)
Appbitb2g_AI          |          ^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1308, in invoke
Appbitb2g_AI          |     return ctx.invoke(self.callback, **ctx.params)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 877, in invoke
Appbitb2g_AI          |     return callback(*args, **kwargs)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/main.py", line 441, in main
Appbitb2g_AI          |     run(
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/main.py", line 609, in run
Appbitb2g_AI          |     config.load_app()
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/config.py", line 415, in load_app
Appbitb2g_AI          |     return import_from_string(self.app)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/uvicorn/importer.py", line 19, in import_from_string
Appbitb2g_AI          |     module = importlib.import_module(module_str)
Appbitb2g_AI          |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
Appbitb2g_AI          |     return _bootstrap._gcd_import(name[level:], package, level)
Appbitb2g_AI          |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
Appbitb2g_AI          |   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
Appbitb2g_AI          |   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
Appbitb2g_AI          |   File "/app/main.py", line 3, in <module>
Appbitb2g_AI          |     from app.core.config import settings
Appbitb2g_AI          |   File "/app/app/core/config.py", line 18, in <module>
Appbitb2g_AI          |     settings = Settings()
Appbitb2g_AI          |                ^^^^^^^^^^
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/pydantic_settings/main.py", line 176, in __init__
Appbitb2g_AI          |     super().__init__(
Appbitb2g_AI          |   File "/usr/local/lib/python3.11/site-packages/pydantic/main.py", line 263, in __init__
Appbitb2g_AI          |     validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
Appbitb2g_AI          |                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Appbitb2g_AI          | pydantic_core._pydantic_core.ValidationError: 5 validation errors for Settings
Appbitb2g_AI          | db_host
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='db', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_port
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='3306', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_name
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='app_bit_b_2g_db', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_user
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='root', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI          | db_password
Appbitb2g_AI          |   Extra inputs are not permitted [type=extra_forbidden, input_value='root', input_type=str]
Appbitb2g_AI          |     For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
Appbitb2g_AI exited with code 1 (restarting)