//	package Networking;

import java.util.Scanner;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.URL;

import java.io.*;

import org.json.*;

public class Networking {

	private static Scanner in;

	public static void main(String[] args) throws Exception{

		//branje stanja
		FileReader file = new FileReader("stanje.txt");
		BufferedReader br = new BufferedReader(file);

		/** odpiranje datoteke markdown **/
		BufferedWriter izhod = new BufferedWriter(new FileWriter("out.md", true));

		//izhod.write("### zdravo");
		izhod.newLine();
		izhod.newLine();

		in = new Scanner(System.in);
		boolean zakljuci = false;
		//while(!zakljuci) {

			String sport = "";
			System.out.println("Izberite katero ligo zelite pregledati	(Izberite ztevilko od 1 do 6)\n");
			System.out.println("1 - Anglezka Premier Liga \n2 - Nemzka Bundes Liga\n3 - Italijanska Seria A\n4 - zpanska La Liga\n5 - Portugalska Premier Liga\n6 - Prva Francoska Liga");
			Scanner sc = new Scanner(System.in);
			int stLige = sc.nextInt();
			switch(stLige) {
			case 1:
				sport = "soccer_epl";
				izhod.write("### Pregledali ste Anglesko premier ligo");
				break;
			case 2:
				sport = "soccer_germany_bundesliga";
				izhod.write("### Pregledali ste nemsko Bundes ligo");
				break;
			case 3:
				sport = "soccer_italy_serie_a";
				izhod.write("### Pregledali ste italiansko Serie A");
				break;
			case 4:
				sport = "soccer_spain_la_liga";
				izhod.write("### Pregledali ste spansko la ligo");
				break;
			case 5:
				sport = "soccer_portugal_primeira_liga";
				izhod.write("### Pregledali ste portugalsko premier ligo");
				break;
			case 6:
				sport = "soccer_france_ligue_one";
				izhod.write("### Pregledali ste prvo francosko ligo");
				break;
			}

			izhod.newLine();
			izhod.newLine();

			String urlLink = "https://api.the-odds-api.com/v3/odds/?sport=" + sport + "&region=uk&mkt=h2h&apiKey=ab9436a91b2eff042f4d1ed03cd11702"; //tuki das link od api-ja
				// ?sport das lahko tut kj druzga, npr 'UPCOMING' ti da naslednjih 8 k pridejo na vrsto
				//?sport=soccer_epl za anglezko ligo || soccer_germany_bundesliga	||	soccer_italy_serie_a	||	soccer_denmark_superliga	||		soccer_spain_la_liga	||	soccer_portugal_primeira_liga	||	icehockey_nhl	||	basketball_nba	||	soccer_france_ligue_one
				//?all = 1 ti vrne vse zporte na vseh podrozjih
			//za stave: https://the-odds-api.com/#get-access


			URL url = new URL(urlLink);
			HttpURLConnection conn =(HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");

			BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
			StringBuffer sb = new StringBuffer();
			String line;
			while((line = in.readLine()) != null) {
				sb.append(line);
			}
			in.close();

			//System.out.println(sb.toString());
			JSONObject obj = new JSONObject(sb.toString());
			JSONArray data = obj.getJSONArray("data");

			double razpolozljivoStanje = Double.parseDouble(br.readLine());
			br.close();
			String optimPrvaEkipa = "";
			String optimDrugaEkipa = "";
			double optimKoeficientProfita = 1;	//tukaj shranjujez najboljzi koeficient profita

			for(int i = 0; i < data.length(); i++) {	//vse tekme/dogodki
				//prva in druga ekipa nima veze kdo je doma kdo pa v gosteh
				JSONObject tekma = data.getJSONObject(i);
				String prvaEkipa = tekma.getJSONArray("teams").getString(0);
				String drugaEkipa = tekma.getJSONArray("teams").getString(1);
				//System.out.println(prvaEkipa + " vs " + drugaEkipa + "\n");

				izhod.write("**Tekma:** `" + prvaEkipa + " VS " + drugaEkipa + "`");
				izhod.newLine();
				izhod.newLine();

				int stStavnic = tekma.getInt("sites_count");
				JSONArray stavnice = tekma.getJSONArray("sites");


				int stMoznihOpcij = stavnice.getJSONObject(1).getJSONObject("odds").getJSONArray("h2h").length();	//to je ubistvu kvote.length(), sam da sm mogu zuni deklarerat(index je 0 ker je posod isto in ni vazn ker je)_______lohka sta 2 al pa 3 opcije za stave...ucasih se vec
				double[][] kvoteTabela = new double[stStavnic][stMoznihOpcij];	//za vsako stavnico zapise kvote
				for(int j = 0; j < stStavnic; j++) {	//vse stavnice
					JSONObject posameznaStavnica = stavnice.getJSONObject(j);
					String imeStavnice = posameznaStavnica.getString("site_nice");
					JSONArray kvote = posameznaStavnica.getJSONObject("odds").getJSONArray("h2h");
					//System.out.print("Ime stavnice: " +  imeStavnice + "   ---   kvote:  ");

					for(int k = 0; k<stMoznihOpcij; k++) {
						double posameznaKvota = kvote.getDouble(k);
						//if smarkets *0.98
						if(imeStavnice.equals("Smarkets") || imeStavnice.equals("Betfair"))
							posameznaKvota *= 0.9;
						kvoteTabela[j][k] = posameznaKvota;
						//System.out.println("Opcija " + k + "     kvota:   " + posameznaKvota);
					}
					//System.out.println(kvote.toString(0) + "  ");
				}

				//tuki zdj poisce najbolse kvote iz vseh stavnic
				double[] topKvote = new double[stMoznihOpcij];
				String[] stavniceTopKvote = new String[stMoznihOpcij];	//na kerih stavnicah so te top kvote
				//za vsako opcijo preletis vse stavnice
				for(int j = 0; j < stMoznihOpcij; j++) {
					for(int k = 0; k < stStavnic; k++) {
						if(kvoteTabela[k][j] > topKvote[j]) {
							topKvote[j] = kvoteTabela[k][j];
							stavniceTopKvote[j] = stavnice.getJSONObject(k).getString("site_nice");	//ime stavnice
						}
					}
				}
				//tuki zdj zrazuna kolk mas profita
				double koeficientProfita = 0;	// ce je koeficient 1, smo na nuli; ze je manjzi smo na plusu, ze je vezji smo v minusu
				for(int j = 0; j < topKvote.length; j++) {
					koeficientProfita += 1/topKvote[j];
				}

				//System.out.println("Najbolsa opcija za stavljenje na to tekmo je :");
				izhod.write("Najbolsa opcija za stavljenje na to tekmo je :");
				izhod.newLine();
				izhod.newLine();

				izhod.write("| Stavnica      | Kvota     | Stavite na    | EUR (polozite)   |");
				izhod.newLine();
				izhod.write("| ------------- |:-------------:| -----:| -----:|");
				for(int j = 0; j < topKvote.length; j++) {
					izhod.newLine();
					double polozim = razpolozljivoStanje/(topKvote[j]*koeficientProfita);
					izhod.write("| "+ stavniceTopKvote[j] + " |" + topKvote[j]+"| " + j + " | " + polozim + " |");
					//System.out.println("Opcija " + j + "-->" + "Stavnica:  " + stavniceTopKvote[j] + "      Kvota: " + topKvote[j]);
				}

				izhod.newLine();
				izhod.newLine();

				//System.out.println("\nze polozite na opcijo:");
				for(int j = 0; j < topKvote.length; j++) {
					double polozim = razpolozljivoStanje/(topKvote[j]*koeficientProfita);
					//System.out.println("zt:" + j + " " + polozim + "EUR");
				}

				//System.out.println("\nBoste na koncu imeli " + razpolozljivoStanje/koeficientProfita + " EUR stanja.  (Zazetno stanje: " + razpolozljivoStanje + ")");

				//tukaj ze priredim optimKoeficientProfita, ze vezji od tedanjega
				if(koeficientProfita < optimKoeficientProfita) {
					optimKoeficientProfita = koeficientProfita;
					optimPrvaEkipa = prvaEkipa;
					optimDrugaEkipa = drugaEkipa;
				}
				izhod.newLine();
				izhod.newLine();
				izhod.write("---");
				izhod.newLine();
				izhod.newLine();
				//System.out.println("\n\n\n");
			}

			if(optimKoeficientProfita < 1) {
				izhod.write("# Pod crto, najbolj se vam spaca staviti na: ");
				izhod.newLine();
				izhod.newLine();
				izhod.write("**TEKMA:**   ");
				izhod.write("**"+ optimPrvaEkipa +"**  VS  **"+ optimDrugaEkipa +"**");
				izhod.newLine();
				izhod.newLine();
				izhod.write("` Iz stanja " + razpolozljivoStanje + "EUR boste prejeli: `" + " **" +razpolozljivoStanje/optimKoeficientProfita + "**" + "EUR");
				izhod.newLine();
				izhod.newLine();
				System.out.println("Najbolj se vam splaza staviti na tekmo med " + optimPrvaEkipa + " in " + optimDrugaEkipa + ", kjer boste s svojega trenutnega stanja: " + razpolozljivoStanje + " EUR   prejeli: " + razpolozljivoStanje/optimKoeficientProfita);
				//System.out.println("Ali boste polozili stavo?   (Da polozite stavo napisite v konzolo znak 'Y', sicer napizite znak 'N')");
				/*String poloziStavo = sc.next();
				if(poloziStavo.equals("Y")) {
					razpolozljivoStanje /= optimKoeficientProfita;
					System.out.println("Vaze posodobljeno stanje je: " + razpolozljivoStanje);
				}
				else if(poloziStavo.equals("N")) {
					System.out.println("Razumljivo. Poskusite ponovno naslednjiz.");
				}
				else {
					System.out.println("Napazen vhod");
				}*/
			}
			else {
				izhod.write("# Zal ni na voljo nobena arbitraza. ");
				izhod.newLine();
				izhod.newLine();
				System.out.println("zal ni na voljo nobena arbitraza, lahko poskusite ze pri drugih zportih -- Vaze trenutno stanje je: " + razpolozljivoStanje);
			}


			//zapisovanje stanja
			//pisanje

			/*File newFile = new File("stanje.txt");
			if(newFile.exists()) {
				newFile.delete();
			}

			try {
				newFile.createNewFile();
			}
			catch(Exception e) {
				e.printStackTrace();
			}
			PrintWriter pw = new PrintWriter(newFile);
			pw.print(razpolozljivoStanje);
			pw.close();*/

			izhod.close();

			//System.out.println("Zakljuzili ste program. ze zelite, ga lahko uporabite ponovno tako, da napizete v konzolo znak 'Y'. ze zelite zakljuziti, vpizite znak 'N'.");
			/*String zakljuciProgram = sc.next();
			if(zakljuciProgram.equals("N")) {
				System.out.println("Zakljuzili ste program.");
				zakljuci = true;
			}
			else if(zakljuciProgram.equals("Y")) {
				System.out.println("Program se bo ponovno zagnal.");
			}
			else {
				System.out.println("Err");
			}*/
		//}
	}

}



/*API KEYS---- free plan sam 150 poizvedb na mesec
 * 906122ac32e5933976ec4400e54eedb5
 *
 * d392a5b3f87f8c523e20083d043cf30d
 * ab9436a91b2eff042f4d1ed03cd11702
 *
 */
