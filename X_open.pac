function FindProxyForURL(url,host)
{

	var hostip = dnsResolve(host);

	if (dnsDomainIs(host, "www.apple.com.cn")) {
				return "PROXY 133.54.5.25:15080";
	} else if (dnsDomainIs(host, "x.com")) {
		return "DIRECT";
	} else if (isInNet(hostip, "104.127.211.121", "255.255.255.255")) {
		return "PROXY 133.54.5.25:15080";
	} else if (isPlainHostName (host) || dnsDomainIs(host, ".apple.com") || dnsDomainIs(host, ".zoom.us")) {
		return "DIRECT";
	} else if (isInNet(hostip, "17.0.0.0", "255.0.0.0")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.apple.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.icloud.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "updates.cdn-apple.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.mzstatic.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.msftidentity.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.msidentity.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "account.activedirectory.windowsazure.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "accounts.accesscontrol.windows.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "adminwebservice.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "api.passwordreset.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "autologon.microsoftazuread-sso.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "becws.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "clientconfig.microsoftonline-p.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "companymanager.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "device.login.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "graph.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "graph.windows.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "login.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "login.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "login.microsoftonline-p.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "login.windows.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "logincert.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "loginex.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "login-us.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "nexus.microsoftonline-p.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "passwordreset.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "provisioningapi.microsoftonline.com")) {
		return "DIRECT";
	} else if (isInNet(hostip, "20.190.128.0", "255.255.192.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "40.126.0.0", "255.255.192.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "40.126.0.0", "255.255.192.0")) {
		return "DIRECT";
	} else if (shExpMatch(host, "meraki.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "ios.meraki.com")) {
		return "DIRECT";
	} else if (isInNet(hostip, "13.210.231.153", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "52.65.84.14", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "209.206.48.0", "255.255.240.0")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.loilo.tv")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.loilonote.app")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.windows.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.msftauth.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.msauth.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.skype.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.office.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.office.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.office365.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.officeapps.live.com")) {
		return "DIRECT";
        } else if (shExpMatch(host, "*.lync.com")) {
                return "DIRECT";
        } else if (shExpMatch(host, "*.teams.microsoft.com")) {
                return "DIRECT";
        } else if (shExpMatch(host, "teams.microsoft.com")) {
                return "DIRECT";
        } else if (shExpMatch(host, "*.keydelivery.mediaservices.windows.net")) {
                return "DIRECT";
        } else if (shExpMatch(host, "*.streaming.mediaservices.windows.net")) {
                return "DIRECT";
        } else if (shExpMatch(host, "mlccdn.blob.core.windows.net")) {
                return "DIRECT";
        } else if (shExpMatch(host, "aka.ms")) {
                return "DIRECT";
        } else if (shExpMatch(host, "*.users.storage.live.com")) {
                return "DIRECT";
        } else if (shExpMatch(host, "adl.windows.com")) {
                return "DIRECT";
        } else if (shExpMatch(host, "*.secure.skypeassets.com")) {
                return "DIRECT";
        } else if (shExpMatch(host, "mlccdnprod.azureedge.net")) {
                return "DIRECT";
        } else if (shExpMatch(host, "*.skype.com")) {
                return "DIRECT";
        } else if (shExpMatch(host, "compass-ssl.microsoft.com")) {
                return "DIRECT";
        } else if (isInNet(hostip, "13.107.64.0", "255.255.192.0")) {
                return "DIRECT";
        } else if (isInNet(hostip, "52.112.0.0", "255.252.0.0")) {
                return "DIRECT";
        } else if (isInNet(hostip, "52.122.0.0", "255.254.0.0")) {
                return "DIRECT";
        } else if (isInNet(hostip, "52.238.119.141", "255.255.255.255")) {
                return "DIRECT";
        } else if (isInNet(hostip, "52.244.160.207", "255.255.255.255")) {
                return "DIRECT";
	} else if (shExpMatch(host, "*.aadrm.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.acompli.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.activity.windows.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.appex-rf.msn.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.appex.bing.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.aria.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.assets-yammer.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.auth.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.azure-apim.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.azureedge.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.azurerms.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.blob.core.windows.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.cloud.microsoft")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.compliance.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.cortana.ai")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.entrust.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.events.data.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.flow.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.geotrust.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.hip.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.informationprotection.azure.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.keydelivery.mediaservices.windows.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.lync.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.mail.protection.outlook.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.media.azure.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.microsoftonline-p.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.microsoftstream.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.microsoftusercontent.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.msauth.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.msauthimages.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.msecnd.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.msftauth.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.msftauthimages.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.msftidentity.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.msidentity.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.msocdn.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.mx.microsoft")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.o365weve.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.office.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.office.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.office365.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.officeapps.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.omniroot.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.onenote.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.online.office.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.onmicrosoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.outlook.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.outlookmobile.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.phonefactor.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.portal.cloudappsecurity.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.powerapps.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.powerautomate.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.protection.office.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.protection.outlook.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.public-trust.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.search.production.apac.trafficmanager.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.search.production.emea.trafficmanager.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.search.production.us.trafficmanager.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.secure.skypeassets.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.security.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.sharepoint.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.sharepointonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.skype.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.static.microsoft")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.streaming.mediaservices.windows.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.svc.ms")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.symcb.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.symcd.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.teams.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.usercontent.microsoft")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.users.storage.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.verisign.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.verisign.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.virtualearth.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.wns.windows.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.yammer.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.yammerusercontent.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*cdn.onenote.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "account.activedirectory.windowsazure.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "account.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "accounts.accesscontrol.windows.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "activation.sls.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "activity.windows.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "adl.windows.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "admin.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "admin.onedrive.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "adminwebservice.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "ajax.aspnetcdn.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "aka.ms")) {
		return "DIRECT";
	} else if (shExpMatch(host, "amp.azure.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "api.passwordreset.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "apis.live.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "apps.identrust.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "appsforoffice.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "assets.onestore.ms")) {
		return "DIRECT";
	} else if (shExpMatch(host, "auth.gfx.ms")) {
		return "DIRECT";
	} else if (shExpMatch(host, "autodiscover.*.onmicrosoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "autologon.microsoftazuread-sso.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "becws.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "c.bing.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "c.bing.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "c.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "c1.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "cacerts.digicert.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "ccs.login.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "cdn.odc.officeapps.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "cdn.uci.officeapps.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "cert.int-x3.letsencrypt.org")) {
		return "DIRECT";
	} else if (shExpMatch(host, "clientconfig.microsoftonline-p.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "companymanager.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "compass-ssl.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "compliance.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "crl.globalsign.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "crl.globalsign.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "crl.identrust.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "crl.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "crl3.digicert.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "crl4.digicert.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "d.docs.live.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "dc.services.visualstudio.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "defender.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "device.login.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "dgps.support.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "docs.live.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "docs.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "ecn.dev.virtualearth.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "enterpriseregistration.windows.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "eus-www.sway-cdn.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "eus-www.sway-extensions.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "firstpartyapps.oaspapps.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "g.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "go.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "graph.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "graph.windows.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "informationprotection.hosting.portal.azure.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "isrg.trustid.ocsp.identrust.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "login-us.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "login.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "login.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "login.microsoftonline-p.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "login.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "login.windows-ppe.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "login.windows.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "logincert.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "loginex.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "mem.gfx.ms")) {
		return "DIRECT";
	} else if (shExpMatch(host, "mlccdn.blob.core.windows.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "mlccdnprod.azureedge.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "mscrl.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "msdn.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "nexus.microsoftonline-p.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "nps.onyx.azure.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "o15.officeredir.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "ocos-office365-s2s.msedge.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "ocsp.digicert.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "ocsp.globalsign.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "ocsp.msocsp.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "ocsp2.globalsign.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "ocspx.digicert.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "office.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "office15client.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "officeapps.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "officecdn.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "officecdn.microsoft.com.edgesuite.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "officeclient.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "officepreviewredir.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "officeredir.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "officespeech.platform.bing.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "oneclient.sfx.ms")) {
		return "DIRECT";
	} else if (shExpMatch(host, "otelrules.azureedge.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "outlook.office.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "outlook.office365.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "partnerservices.getmicrosoftkey.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "passwordreset.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "platform.linkedin.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "policykeyservice.dc.ad.msft.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "prod.firstpartyapps.oaspapps.com.akadns.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "prod.msocdn.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "protection.office.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "provisioningapi.microsoftonline.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "r.office.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "secure.globalsign.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "security.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "shellprod.msocdn.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "signup.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "smtp.office365.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "spoprod-a.akamaihd.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "ssw.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "staffhub.ms")) {
		return "DIRECT";
	} else if (shExpMatch(host, "storage.live.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "support.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "sway.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "teams.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "technet.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "telemetryservice.firstpartyapps.oaspapps.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "tse1.mm.bing.net")) {
		return "DIRECT";
	} else if (shExpMatch(host, "wus-firstpartyapps.oaspapps.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "wus-www.sway-cdn.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "wus-www.sway-extensions.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "www.acompli.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "www.bing.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "www.digicert.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "www.microsoft.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "www.microsoft365.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "www.onedrive.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "www.outlook.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "www.sway.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "manaviewer.jp")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-2.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-3.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-4.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-5.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-oplog.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-oplog-2.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-oplog-3.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-oplog-4.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-oplog-5.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-stdlog.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-stdlog-2.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-stdlog-3.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-stdlog-4.servicebus.windows.net")) {
              return "DIRECT";
	} else if (shExpMatch(host, "manaviewer-prd-stdlog-5.servicebus.windows.net")) {
              return "DIRECT";
	} else if (isInNet(hostip, "104.146.128.0", "255.255.128.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "104.47.0.0", "255.255.128.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "13.107.128.0", "255.255.252.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "13.107.136.0", "255.255.252.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "13.107.140.6", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "13.107.18.10", "255.255.255.254")) {
		return "DIRECT";
	} else if (isInNet(hostip, "13.107.18.15", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "13.107.6.152", "255.255.255.254")) {
		return "DIRECT";
	} else if (isInNet(hostip, "13.107.6.171", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "13.107.6.192", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "13.107.64.0", "255.255.192.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "13.107.9.192", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "131.253.33.215", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "132.245.0.0", "255.255.0.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "150.171.32.0", "255.255.252.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "150.171.40.0", "255.255.252.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "20.190.128.0", "255.255.192.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "20.20.32.0", "255.255.224.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "20.231.128.0", "255.255.224.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "204.79.197.215", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "23.103.160.0", "255.255.240.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "40.104.0.0", "255.254.0.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "40.107.0.0", "255.255.0.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "40.108.128.0", "255.255.128.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "40.126.0.0", "255.255.192.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "40.92.0.0", "255.254.0.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "40.96.0.0", "255.248.0.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "52.100.0.0", "255.252.0.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "52.104.0.0", "255.252.0.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "52.108.0.0", "255.252.0.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "52.112.0.0", "255.252.0.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "52.122.0.0", "255.254.0.0")) {
		return "DIRECT";
	} else if (isInNet(hostip, "52.238.119.141", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "52.238.78.88", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "52.244.160.207", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "52.244.37.168", "255.255.255.255")) {
		return "DIRECT";
	} else if (isInNet(hostip, "52.96.0.0", "255.252.0.0")) {
		return "DIRECT";
	} else if (shExpMatch(host, "storage.googleapis.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "firebase.google.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "accounts.google.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "www.gstatic.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "firebase.googleapis.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.ingest.sentry.io")) {
		return "DIRECT";
	} else if (shExpMatch(host, "qubena-s.app")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.qubena-s.app")) {
		return "DIRECT";
	} else if (shExpMatch(host, "qubena.app")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.qubena.app")) {
		return "DIRECT";
	} else if (shExpMatch(host, "qubena-m.app")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.qubena-m.app")) {
		return "DIRECT";
	} else if (shExpMatch(host, "qubena.com")) {
		return "DIRECT";
	} else if (shExpMatch(host, "*.qubena.com")) {
		return "DIRECT";
	} else {
		return "PROXY 133.54.5.25:15080";
	}
}

