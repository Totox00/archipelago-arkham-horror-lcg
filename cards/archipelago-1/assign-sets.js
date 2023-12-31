// automatically assigns the set and collection images to all components in project

const encounterSets = [];
const addedSets = [];

/*
forAll(project, function (member) {
    if (member.name.endsWith(".eon")) {
    	const name = member.parent.file.toString().split("archipelago-1/")[1];
    	if (!addedSets.includes(name)) {
    		encounterSets.push({
	    		name: name,
	    		icon: `${member.parent.file.toString().replace("archipelago-1", "img")}/set.svg`,
	    		tag: name
	    	});
	    	addedSets.push(name);
    	}
    }
});

println(encounterSets.map(a => `name: ${a.name}, icon: ${a.icon}, tag: ${a.tag}`).join("\n"));
println(addedSets.join("\n"));

const settings = Settings.getUser();
settings.set("AHLCG-UserEncounterCount", encounterSets.length);
for (let i = 0; i < encounterSets.length; i++) {
	println(`Created set ${encounterSets[i].name} with icon ${encounterSets[i].icon}`);
	settings.set(`AHLCG-UserEncounterIcon${i+1}`, encounterSets[i].icon);
	settings.set(`AHLCG-UserEncounterName${i+1}`, encounterSets[i].name);
	settings.set(`AHLCG-UserEncounterTag${i+1}`, encounterSets[i].tag);
}
*/
var collectionIndex = 0;
var encounterIndex = {};

forAll(project, function (member) {
    if (member.name.endsWith(".eon")) {
    	const file = member.file;
    	const component = ResourceKit.getGameComponentFromFile(member.file);
    	println(`Updating component ${file}...`);
       
        // collection
    	collectionIndex++;
		component.settings.set("Collection", "Archipelago");
		component.settings.set("CollectionNumber", collectionIndex);
		
		// encounter
		const encounterSet = member.parent.file.toString().split("archipelago-1/")[1];
		if (!encounterIndex[encounterSet]) {encounterIndex[encounterSet] = 0;}
		encounterIndex[encounterSet]++;
		// component.settings.set("Encounter", encounterSet);
		component.settings.set("EncounterNumber", encounterIndex[encounterSet]);
    
        ResourceKit.writeGameComponentToFile(file, component);
        member.synchronize();
    }
});

forAll(project, function (member) {
    if (member.name.endsWith(".eon")) {
    	const file = member.file;
    	const component = ResourceKit.getGameComponentFromFile(member.file);
   
		// encounter total
		const encounterSet = member.parent.file.toString().split("archipelago-1/")[1];
		component.settings.set("EncounterTotal", encounterIndex[encounterSet]);
    
        ResourceKit.writeGameComponentToFile(file, component);
        member.synchronize();
    }
});

importClass(java.io.File);
importPackage(arkham.project);

function forAll(parent, somethingToDo) {
    var i;
    var child;
    var children = parent.getChildren();
    for (i = 0; i < children.length; ++i) {
        child = children[i];
        if (child.isFolder()) {
            forAll(child, somethingToDo);
        }
        somethingToDo(child);
    }
    parent.synchronize();
}
