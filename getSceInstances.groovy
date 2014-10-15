import com.sohu.sce.api.model.AppInstance;
import com.sohu.sce.api.model.Credentials;
import com.sohu.sce.api.service.AppService;
import com.sohu.sce.api.service.ServiceFactory;
import java.util.List;


def getInstanceList(appId,secret){

        Credentials c = new Credentials(appId,secret);
        AppService service = ServiceFactory.getInstance();
        service.setEndPoint("http://sceapi.apps.sohuno.com/");
        List<AppInstance> list = service.findInstances(c, Integer.parseInt(appId));
        StringBuilder sb = new StringBuilder();
        String ret = "";
        for(AppInstance app: list) {
            sb.append(app.getIp()).append(",");
        }
        if(sb.length()>0)
            sb.deleteCharAt(sb.length()-1);
        return sb.toString(); 
}

print getInstanceList(this.args[0],this.args[1]);
